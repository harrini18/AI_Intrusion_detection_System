import tensorflow as tf
import pickle
import numpy as np

# Step 1: Load the trained model
print("Loading trained model...")
model = tf.keras.models.load_model("trained_model.h5")

# Step 2: Convert the model to TensorFlow Lite format
print("Converting model to TensorFlow Lite format...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the converted model
tflite_model_path = "trained_model.tflite"
with open(tflite_model_path, "wb") as f:
    f.write(tflite_model)
print(f"Model saved as {tflite_model_path}")

# Step 3: Optimize for TinyML (Quantization)
print("Applying quantization for TinyML...")
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_quant_model = converter.convert()

# Save the quantized model
tflite_quant_model_path = "trained_model_quant.tflite"
with open(tflite_quant_model_path, "wb") as f:
    f.write(tflite_quant_model)
print(f"Quantized model saved as {tflite_quant_model_path}")

# Step 4: Convert scaler.pkl to C++ array
print("Converting scaler.pkl to C++ format...")
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Extract mean and scale values from the StandardScaler
means = scaler.mean_
scales = scaler.scale_

# Generate C++ header file content
cpp_code = f"""
#ifndef SCALER_CONSTANTS_H
#define SCALER_CONSTANTS_H

const float means[] = {{{', '.join(map(str, means))}}};
const float scales[] = {{{', '.join(map(str, scales))}}};

#endif // SCALER_CONSTANTS_H
"""

# Save as a header file
cpp_file_path = "scaler_constants.h"
with open(cpp_file_path, "w") as f:
    f.write(cpp_code)
print(f"Scaler constants saved as {cpp_file_path}")

print("\nConversion completed successfully!")
