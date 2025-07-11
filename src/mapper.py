def get_scale(world_size, layer_size):
    return world_size / layer_size

def world_to_pixel(x, z, world_size, layer_size):
    scale = get_scale(world_size, layer_size)
    px = int(x / scale)
    py = layer_size - int(z / scale)
    return px, py
