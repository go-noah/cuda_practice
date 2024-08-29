# Usage: python bin2img_fp32.py <path/to/output.bin> <path/to/output.png>
# Description: Convert a binary file to a PNG image

# Executable generation: pyinstaller --onefile bin2img_fp32.py

import sys
import numpy as np
from PIL import Image

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print("Usage: python bin2img_fp32.py "
          "<path/to/output.bin> "
          "<path/to/output.png>")
    sys.exit(1)

  input_path = sys.argv[1]
  output_path = sys.argv[2]

  # Load input from a binary file
  with open(input_path, "rb") as f:
    input_bin = f.read()

  # Only first (3 x 128 x 128) values are considered
  input_bin = input_bin[:3 * 128 * 128 * 4] # 4 Bytes per float

  # Convert binary data to numpy array
  input_array = np.frombuffer(input_bin, dtype=np.float32)

  # Reshape the array to (3, 128, 128) for a 128x128 RGB image
  input_array = input_array.reshape(3, 128, 128)

  # Normalize the data to the range [0, 255]
  input_array = (input_array - input_array.min()) / (input_array.max() - 
                input_array.min()) * 255.0

  # Convert numpy array to uint8
  input_array = input_array.astype(np.uint8)

  # Convert the numpy array to a PIL Image with RGB mode
  output_image = Image.fromarray(np.transpose(input_array, (1, 2, 0)), 'RGB')

  # Save the image
  output_image.save(output_path)
