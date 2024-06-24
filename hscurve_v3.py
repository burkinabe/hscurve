import numpy as np
from PIL import Image
import math

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

# Example usage:
generate_hilbert_image('OfficeSetup.exe', 800, 600, 'output_image_v3.png')
