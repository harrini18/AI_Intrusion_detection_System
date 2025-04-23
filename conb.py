import numpy as np

# Read the TFLite model
tflite_model_path = "trained_model.tflite"
header_file_path = "model.h"

print(f"Reading {tflite_model_path}...")
with open(tflite_model_path, "rb") as f:
    tflite_model = f.read()

# Convert to a C++ byte array
tflite_model_hex = ', '.join(f'0x{byte:02X}' for byte in tflite_model)

# Generate the C++ header file
cpp_code = f"""
#ifndef MODEL_H
#define MODEL_H

#include <cstdint>

const unsigned char model_tflite[] = {{
    {tflite_model_hex}
}};

const unsigned int model_tflite_len = {len(tflite_model)};

#endif // MODEL_H
"""

# Save the header file
with open(header_file_path, "w") as f:
    f.write(cpp_code)

print(f"Model successfully converted and saved as {header_file_path}")
