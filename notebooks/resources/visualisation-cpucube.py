import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a 3D numpy array with zeros
cube = np.zeros((8, 8, 8))

# Create a figure
fig = plt.figure()

# Add a subplot
ax = fig.add_subplot(111, projection='3d')

# Set initial color to red
color = 'r'

# Set initial view and limits
ax.view_init(elev=20., azim=30)
ax.set_xlim(0, 8)
ax.set_ylim(0, 8)
ax.set_zlim(0, 8)

# Create a directory to store the PNG frames (change 'frames' to your desired directory)
import os
if not os.path.exists('frames'):
    os.makedirs('frames')

frame_number = 0  # Initialize frame number

# Iterate over the array and change color each second
for z in range(8):
    for x in range(8):
        for y in range(8):
            # Set the color of the voxel
            cube[x, y, z] = 1

            # Pause for one second
            plt.pause(0.01)

            # Show the updated plot
            ax.voxels(cube, facecolors=color, edgecolors='k')
            ax.set_axis_off()

            # Save the current frame as a PNG image
            frame_filename = f'frames/frame_{frame_number:04d}.png'
            plt.savefig(frame_filename)
            frame_number += 1

# Plot the cube with the final state
ax.voxels(cube, facecolors=color, edgecolors='k')

# Save the final frame as a PNG image
frame_filename = f'frames/frame_{frame_number:04d}.png'
plt.savefig(frame_filename)

# Show the final plot
plt.show()
