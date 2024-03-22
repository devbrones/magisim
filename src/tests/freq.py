#import numpy as np
#import matplotlib.pyplot as plt
#
#grid = np.zeros((400, 200))
#
#
#x, y = np.arange(-200, 200, 1), np.arange(190, 200, 1)
#X, Y = np.meshgrid(x, y)
#lens_mask = X ** 2 + Y ** 2 <= 40000
#for j, col in enumerate(lens_mask.T):
#    for i, val in enumerate(np.flip(col)):
#        if val:
#            # Modify grid assignments for biconcave lenses accordingly
#            grid[130 + i : 150 - i, j - 100 : j - 99] = 1
#            break
#
#
##y, x = np.ogrid[:200, :200]
##y = y[::-1]
##
##lmask2 = ((x - 20//2)**2 + (y-20//2)**2)>= 10**2
##for j, col in enumerate(lens_mask.T):
##    for i, val in enumerate(np.flip(col)):
##        if val:
##            # Modify grid assignments for biconcave lenses accordingly
##            grid[200 + i : 250 - i, j - 100 : j - 99] = 1
##            break
#
#x, y = np.arange(-200, 200, 1), np.arange(190, 200, 1)
#X, Y = np.meshgrid(x, y)
#lens_mask1 = (X ** 2 + Y ** 2 >= 100**2)  # First concave part
#lens_mask2 = (((X - 50) ** 2 + Y ** 2) >= 100**2)  # Second concave part
#
#biconcave_lens_mask = np.logical_and(lens_mask1, lens_mask2)
#
#for j, col in enumerate(biconcave_lens_mask.T):
#    for i, val in enumerate(np.flip(col)):
#        if val:
#            grid[200 + i : 250 - i, j - 100 : j - 99] = 1
#            break
## visualise the grid with matplotlib
#
#plt.imshow(grid, interpolation="nearest")
#plt.show()


import numpy as np
import matplotlib.pyplot as plt

# Define the dimensions of the 2D array
width = 100  # Width of the 2D array
height = 100  # Height of the 2D array

# Create a meshgrid for the x and y coordinates
x = np.linspace(-5, 5, width)
y = np.linspace(-5, 5, height)
X, Y = np.meshgrid(x, y)

# Define the equation for the biconcave lens
radius = 50.0  # Radius of the semi-circular curves
# create the rectangle in the grid

c1 = np.where((X + 55)**2 + Y**2 < radius**2, 1, 0)
c2 = np.where((X - 55)**2 + Y**2 < radius**2, 1, 0)
# create a rectangle and subtract the two circles from it
lens = abs(np.where((X >= -10) & (X <= 10) & (Y >= -20) & (Y <= 20), 1, 0) - c1 - c2)
# cut off outside of rectangle
lens = np.where((X >= -10) & (X <= 10) & (Y >= -20) & (Y <= 20), lens, 0)

# Display the biconcave lens
plt.imshow(lens, cmap='gray', extent=(-5, 5, -5, 5))
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Biconcave Lens')
plt.colorbar(label='Intensity')
plt.show()


