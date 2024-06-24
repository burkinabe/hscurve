import numpy as np
from PIL import Image
import math
import os

def calculate_hilbert_coordinates(index, order):
    def last2bits(x):
        return x & 3

    def shift_right(x, n):
        return x >> n

    positions = [(0, 0), (0, 1), (1, 1), (1, 0)]
    idx = last2bits(index)
    x, y = positions[idx]

    for j in range(1, order + 1):
        index = shift_right(index, 2)
        n = 2 ** j
        idx = last2bits(index)

        if idx == 0:
            x, y = y, x
        elif idx == 1:
            x, y = x, y + n
        elif idx == 2:
            x, y = x + n, y + n
        else:  # idx == 3
            tmp = y
            y = (n - 1) - x
            x = (n - 1) - tmp
            x += n

    return x, y

def generate_hilbert_image(file_path, width, height, output_path):
    with open(file_path, 'rb') as f:
        byteStream = f.read()

    len_bytes = len(byteStream)
    order = math.ceil(math.log2(len_bytes) / 2)
    size = 2 ** order
    pad_len = size * size - len_bytes
    byteStream += bytes(pad_len)

    img_array = np.zeros((size, size), dtype=np.uint8)

    for index in range(len_bytes):
        x, y = calculate_hilbert_coordinates(index, order)
        img_array[x, y] = byteStream[index]

    img = Image.fromarray(img_array, 'L')
    img = img.resize((width, height), resample=Image.Resampling.LANCZOS)
    img.save(output_path)


def process_directory(input_dir, output_dir, width, height):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.exe'):
                input_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_dir)
                output_subdir = os.path.join(output_dir, relative_path)
                if not os.path.exists(output_subdir):
                    os.makedirs(output_subdir)

                output_file_path = os.path.join(output_subdir, f"{os.path.splitext(file)[0]}.png")
                generate_hilbert_image(input_file_path, width, height, output_file_path)
                print(f"Processed {input_file_path} -> {output_file_path}")

# Example usage:
# Replace 'input_directory' and 'output_directory' with your actual directories.
input_directory = 'path/to/input_directory'
output_directory = 'path/to/output_directory'
image_width = 800
image_height = 600

process_directory(input_directory, output_directory, image_width, image_height)