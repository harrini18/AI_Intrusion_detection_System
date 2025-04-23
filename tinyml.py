import numpy as np
import tensorflow as tf
import pickle

# Load the TFLite model
tflite_model_path = "trained_model.tflite"
interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

# Get input and output tensor details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load scaler (for input normalization)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Define sample input data (Replace with real input features)
raw_input_data = np.array([[1200.0, 3.5, 2.0]])  # Example input features

# Normalize input using the scaler
normalized_input = scaler.transform(raw_input_data)

# Set the input tensor
interpreter.set_tensor(input_details[0]['index'], normalized_input.astype(np.float32))

# Run inference
interpreter.invoke()

# Get the output tensor
prediction = interpreter.get_tensor(output_details[0]['index'])

# Display the prediction result
print(f"Predicted Value: {prediction[0][0]}")
