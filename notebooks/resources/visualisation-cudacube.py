import numpy as np
import matplotlib.pyplot as plt

# Create a 3D numpy array with zeros
cube = np.zeros((8, 8, 8))

# Create a figure
fig = plt.figure()

# Set initial color to red
color = 'r'

# Iterate over the array and change color after each plane
for z in range(8):
    for x in range(8):
        for y in range(8):
            # Set the color of the voxel
            cube[x, y, z] = 1

    # Add a subplot
    ax = fig.add_subplot(111, projection='3d')

    # Plot the cube for the current plane
    ax.voxels(cube, facecolors=color, edgecolors='k')

    # Set initial view
    ax.view_init(elev=20., azim=30)

    # Set initial limits
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.set_zlim(0, 8)

    # Save the plot as a PNG image
    filename = f"frame_{z:02d}.png"
    plt.savefig(filename)

    # Clear the subplot for the next frame
    plt.clf()

    # Pause for one second
    plt.pause(0.5)

# Close the figure
plt.close()
