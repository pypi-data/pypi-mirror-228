#include "akida/program_info.h"

#include <cstring>

#include "akida/hw_version.h"
#include "akida/shape.h"
#include "akida/version.h"

#include "engine/dma.h"
#include "infra/system.h"

#include "flatbuffers/base.h"

#include "engine/akida_device_program_fb_generated.h"
#include "engine/akida_program_info_generated.h"

namespace akida {

ProgramInfo::ProgramInfo() : program_data_{nullptr, 0}, program_(nullptr) {}

ProgramInfo::ProgramInfo(const uint8_t* serialized_program_buffer,
                         [[maybe_unused]] size_t serialized_program_size)
    : ProgramInfo() {
  if (!serialized_program_buffer) {
    panic("Program is null");
  }
  // Serialized program is now split in 2 parts: program_info and program
  // (data). 1st part in the buffer is program_info, then program. Both are size
  // prefixed, that means there is a uoffset_t word at the begining of the
  // buffer that contains the size of the actual flatbuffer data. The full size
  // is then this size + sizeof(uoffset_t).
  const auto program_info_size =
      flatbuffers::ReadScalar<flatbuffers::uoffset_t>(
          serialized_program_buffer) +
      sizeof(flatbuffers::uoffset_t);
  // 1st verify program info
  flatbuffers::Verifier program_info_verifier(serialized_program_buffer,
                                              program_info_size);
  auto* program_info =
      fb::GetSizePrefixedProgramInfo(serialized_program_buffer);
  if (program_info == nullptr ||
      fb::VerifySizePrefixedProgramInfoBuffer(program_info_verifier) == false) {
    panic("Unable to parse program info");
  }

  // Then verify program buffer that is located after the program_info part
  const auto* program_data_ptr = serialized_program_buffer + program_info_size;
  // Program flatbuffer is size prefixed, that means there is a uoffset_t word
  // at the begining of the buffer that contains the size of the actual
  // flatbuffer data. The full size is then this size + sizeof(uoffset_t)
  const auto program_data_size =
      flatbuffers::ReadScalar<flatbuffers::uoffset_t>(program_data_ptr) +
      sizeof(flatbuffers::uoffset_t);
  flatbuffers::Verifier program_verifier(program_data_ptr, program_data_size);
  if (fb::VerifySizePrefixedProgramBuffer(program_verifier) == false) {
    panic("Unable to parse program");
  }

  // size of buffer should be equal to the sum of both flatbuffers size (+ size
  // words)
  assert((program_info_size + program_data_size == serialized_program_size) &&
         "Unexpected program buffer size");

  auto* program = fb::GetSizePrefixedProgram(program_data_ptr);
  // Check that the akida version this program was compiled with matches the
  // current version.
  const auto& program_version = program_info->version()->c_str();
  const auto& lib_version = version();
  if (strcmp(program_version, lib_version) != 0) {
    panic("Program version [%s] does not match library version [%s]",
          program_version, lib_version);
  }

  // store info about the program parts
  program_data_ = {program_data_ptr, program_data_size};
  program_ = program;
  program_info_ = program_info;
}

HwVersion ProgramInfo::device_version() const {
  const auto* fb_device_version = program_info_->device_version();

  return HwVersion{
      fb_device_version->vendor_id(), fb_device_version->product_id(),
      fb_device_version->major_rev(), fb_device_version->minor_rev()};
}

const uint32_t* ProgramInfo::input_dims() const {
  return program_info_->input_dims()->data();
}

Shape ProgramInfo::output_dims() const {
  const auto& output_dims = *program_info_->output_dims();
  return Shape{output_dims[0], output_dims[1], output_dims[2]};
}

bool ProgramInfo::input_is_dense() const {
  return program_info_->input_type() == fb::IoType_dense;
}

bool ProgramInfo::output_is_dense() const {
  return program_info_->output_type() == fb::IoType_dense;
}

bool ProgramInfo::activation_enabled() const {
  return program_info_->activation();
}

uint32_t ProgramInfo::dense_input_window_width() const {
  return program_info_->dense_window_w();
}

uint32_t ProgramInfo::dense_input_window_height() const {
  return program_info_->dense_window_h();
}

bool ProgramInfo::can_learn() const {
  return program_->learning_layer() != nullptr;
}

uint32_t ProgramInfo::learn_weights_word_size() const {
  const auto* learning_layer = program_->learning_layer();
  // learn_mem_size is the number of 32 bits words required by learn memory
  return learning_layer != nullptr ? learning_layer->learn_mem_size() : 0;
}

uint8_t ProgramInfo::number_of_descriptors_per_pass() const {
  return program_info_->max_num_desc();
}

uint32_t ProgramInfo::number_of_passes() const {
  return program_->passes()->size();
}

uint32_t ProgramInfo::number_of_program_descriptors_required() const {
  const auto nb_passes = number_of_passes();
  return nb_passes > 1 ? nb_passes * number_of_descriptors_per_pass()
                       : dma::kMinNbDescriptors;
}

uint32_t ProgramInfo::number_of_extra_program_descriptors_required() const {
  // There is an extra descriptor if leaning is running on FNP3 during a
  // multipass program
  return (number_of_passes() > 1 && learning_on_fnp3()) ? 1 : 0;
}

bool ProgramInfo::learning_on_fnp3() const {
  return program_->learning_layer() != nullptr &&
         program_->learning_layer()->ram()->np_tracks() != nullptr &&
         program_->learning_layer()->ram()->fnp2_track() == nullptr;
}

static size_t record_np_tracks_byte_size(const fb::Record& record) {
  size_t result = 0;
  // get size of np tracks
  for (const auto* np_track : *record.np_tracks()) {
    result += np_track->data()->size() * sizeof(uint32_t);
  }
  return result;
}

static size_t largest_np_track_byte_size(const fb::Record& record) {
  size_t result = 0;
  for (const auto* np_track : *record.np_tracks()) {
    result = std::max(result, static_cast<size_t>(np_track->data()->size()) *
                                  sizeof(uint32_t));
  }
  return result;
}

size_t ProgramInfo::program_data_required_memory() const {
  size_t result = 0;
  const auto nb_passes = number_of_passes();
  if (nb_passes > 1) {
    // in multipass, all np tracks must be in memory
    for (const auto* pass : *program_->passes()) {
      for (const auto* record : *pass->records()) {
        result += record_np_tracks_byte_size(*record);
      }
    }
    // if there is learning records we need to count it as well
    const auto* learn = program_->learning_layer();
    if (learn) {
      // learn have both inference & learning tracks, plus weights
      result += record_np_tracks_byte_size(*learn->inference_registers());
      result += record_np_tracks_byte_size(*learn->learning_registers());
      result += record_np_tracks_byte_size(*learn->ram());
    }
  } else {
    // in single pass, tracks are played once at a time, so the required memory
    // is the size of the largest one
    const auto* pass = (*program_->passes())[0];
    for (const auto* record : *pass->records()) {
      result = std::max(result, largest_np_track_byte_size(*record));
    }
    // check if there are learning records
    const auto learn = program_->learning_layer();
    if (learn) {
      result = std::max(
          result, largest_np_track_byte_size(*learn->inference_registers()));
      result = std::max(
          result, largest_np_track_byte_size(*learn->learning_registers()));
      result = std::max(result, largest_np_track_byte_size(*learn->ram()));
    }
  }
  return result;
}

size_t ProgramInfo::fnp2_required_memory() const {
  size_t result = 0;

  // iterate over all records from all passes
  for (const auto* pass : *program_->passes()) {
    for (const auto* record : *pass->records()) {
      // check if we have FNP2 weights
      if (record->fnp2_track()) {
        result += static_cast<size_t>(record->fnp2_track()->data()->size()) *
                  sizeof(uint32_t);
      }
    }
  }
  // check if there is learning records that could contain FNP2
  const auto learn = program_->learning_layer();
  if (learn) {
    // learning/inference registers should not contain FNP2 track
    assert(learn->inference_registers()->fnp2_track() == nullptr);
    assert(learn->learning_registers()->fnp2_track() == nullptr);
    // but ram could
    if (learn->ram()->fnp2_track()) {
      result +=
          static_cast<size_t>(learn->ram()->fnp2_track()->data()->size()) *
          sizeof(uint32_t);
    }
  }
  return result;
}

akida::span<int32_t> akida::ProgramInfo::shifts() const {
  const auto* shifts_vector = program_info_->shifts();
  return {shifts_vector->data(), shifts_vector->size()};
}

akida::span<float> ProgramInfo::scales() const {
  const auto* scales_vector = program_info_->scales();
  return {scales_vector->data(), scales_vector->size()};
}

fb::IoType ProgramInfo::inputs_type() const {
  return program_info_->input_type();
}

fb::IoType ProgramInfo::outputs_type() const {
  return program_info_->output_type();
}

}  // namespace akida
