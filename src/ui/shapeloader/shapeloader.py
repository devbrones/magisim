import numpy as np
from stl import mesh
import matplotlib.pyplot as plt
import trimesh



class ShapeLoader:

    @staticmethod
    
    def voxelization(input_stl_file, voxel_size):
        # Load the STL file
        mesh = trimesh.load_mesh(input_stl_file)
        print("loaded mesh")
        assert(mesh.is_watertight) # you cannot build a solid if your volume is not tight
        volume = mesh.voxelized(pitch=voxel_size/100)
        print("voxelized mesh")
        mat = volume.matrix # matrix of boolean

        return mat

    @staticmethod
    def create(input_stl_file, modeselector, res, cutpoint=None, xpos=0, ypos=0, output_xyz_file=None):
        # Voxelize the input STL file
        voxel_grid = ShapeLoader.voxelization(input_stl_file, res)
        print("loaded voxel grid")

        if modeselector == "1D (single cut)":
            if cutpoint is None:
                raise ValueError("For '1D (single cut)' mode, a 'cutpoint' (y-coordinate) must be specified.")
            # Grab a vertical slice of the 3D array at the specified y-coordinate (cutpoint)
            slice_data = voxel_grid[:, cutpoint, :]

        elif modeselector == "2D (multi cut)":
            if cutpoint is None:
                raise ValueError("For '2D (multi cut)' mode, a 'cutpoint' (x-coordinate) must be specified.")
            # Grab a horizontal slice of the array at the specified x-coordinate (cutpoint)
            slice_data = voxel_grid[cutpoint, :, :]

        elif modeselector == "3D (full)":
            # Return the full 3D array
            slice_data = voxel_grid

        else:
            raise ValueError("Invalid modeselector value. Expected '1D (single cut)', '2D (multi cut)', or '3D (full)'.")

        # Shift the slice data in the x and y directions
        shifted_slice_data = np.roll(slice_data, (xpos, ypos), axis=(0, 1))

        if output_xyz_file:
            # Export the voxel data to an XYZ file
            np.savetxt(output_xyz_file, np.column_stack(np.where(shifted_slice_data)), delimiter=" ", fmt="%d")

        return shifted_slice_data
    
    def create_plot(voxel_data):
        print('dims::: '+str(voxel_data.ndim))
        if voxel_data.ndim == 3:
            print('3d')
            # Create a 3D plot of the voxel data
            fig = plt.figure()
            print('created fig')
            ax = fig.add_subplot(111, projection='3d')
            print('created ax')
            x, y, z = np.indices(voxel_data.shape)
            print('created x,y,z')
            ax.voxels(voxel_data, facecolors='blue', edgecolor='k')
            print('created voxels')
        elif voxel_data.ndim == 2:
            print('2d')
            # Create a 2D plot of the voxel data
            plt.imshow(voxel_data, cmap='gray')
            print('created imshow')
        else:
            raise ValueError("Invalid voxel data shape. Expected 2D or 3D array.")
        return plt

    
    def create_result(input_stl_file, modeselector, res, cutpoint=None, xpos=0, ypos=0, output_xyz_file=None):
        return ShapeLoader.create_plot(ShapeLoader.create(input_stl_file, modeselector, res, cutpoint, xpos, ypos, output_xyz_file))