import math
import numpy as np
from scipy.ndimage import zoom
from PIL import Image
import hilbert


def exe_to_byte_stream(exe_path):
    with open(exe_path, 'rb') as f:
        return f.read()


def calculate_hilbert_coordinates(hilberts, index, order):
    return hilbert.decode(hilberts, num_dims=index, num_bits=2 ** order)


def generate_2d_grayscale_image(shape):
    return np.zeros(shape, dtype=np.uint8)


def main(exe_path, width, height, output_path):
    # Step 1: Convert the EXE file to a byte stream
    byte_stream = exe_to_byte_stream(exe_path)
    len_byte_stream = len(byte_stream)

    # Step 2: Determine the length of the byte stream
    order = math.ceil(math.log2(len_byte_stream) / 2)
    size = 2 ** order

    # Step 3: Pad the byte stream with zeros to fit the calculated size
    pad_len = size * size - len_byte_stream
    byte_stream += bytes([0] * pad_len)

    # Step 4: Create an empty 2D gray-scale image
    img = generate_2d_grayscale_image((size, size))

    # Step 5: Map the byte stream to the image using Hilbert curve coordinates
    for index in range(len_byte_stream):
        x, y = calculate_hilbert_coordinates(byte_stream[index], 2, 3)
        img[x, y] = byte_stream[index]

    # Step 6: Resize the image to the specified dimensions
    resized_img = zoom(img, (height / size, width / size), order=1)

    # Step 7: Save the image in the specified format
    final_img = Image.fromarray(resized_img)
    final_img.save(output_path)


# Example usage
exe_path = 'OfficeSetup.exe'
output_path = 'output_image.png'
width = 256
height = 256
main(exe_path, width, height, output_path)
