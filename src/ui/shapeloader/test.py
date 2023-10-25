import ezdxf
import numpy as np

def dxf_to_numpy(dxf_file_path, width, height, scale=1.0):
    # Create a NumPy array filled with False (air) by default
    numpy_array = np.full((height, width), False, dtype=bool)

    doc = ezdxf.readfile(dxf_file_path)
    msp = doc.modelspace()

    for entity in msp.query('SOLID'):
        vertices = entity.points()
        for y in range(height):
            for x in range(width):
                px = x / scale
                py = y / scale
                if is_inside_solid(vertices, px, py):
                    numpy_array[y, x] = True

    return numpy_array

def is_inside_solid(vertices, x, y):
    # Check if a point (x, y) is inside the solid defined by vertices
    count = 0
    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            count += 1
    return count % 2 == 1

# Example usage:
dxf_file_path = 'bridge.dxf'
width = 100  # Width of the output numpy array
height = 100  # Height of the output numpy array
scale = 1.0  # Scale factor (modify as needed)
result = dxf_to_numpy(dxf_file_path, width, height, scale)
print(result) 