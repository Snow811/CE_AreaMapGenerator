from src.mapper import world_to_pixel
from PIL import Image
import numpy as np
import math

def create_blank_mask(layer_size):
    return np.zeros((layer_size, layer_size), dtype=np.uint8)

def rotate_point(x, z, angle_deg):
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    rx = x * cos_a - z * sin_a
    rz = x * sin_a + z * cos_a
    return rx, rz

def paint_mask(mask, positions, world_size, layer_size):
    for p in positions:
        ox, oz = rotate_point(p["offset_x"], p["offset_z"], p["rotation"])
        wx = p["x"] + ox
        wz = p["z"] + oz
        px, py = world_to_pixel(wx, wz, world_size, layer_size)
        if 0 <= px < layer_size and 0 <= py < layer_size:
            mask[py, px] = 255

def save_mask(mask, output_path):
    img = Image.fromarray(mask, mode='L')
    img.save(output_path, format='TGA')
