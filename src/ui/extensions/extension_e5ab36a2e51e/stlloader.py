import stltovoxel
import stl
import numpy as np
import matplotlib.pyplot as plt
from shared.router import Router, Tunnel
from shared.libmso import mso, SimpleObject
import tempfile

stlloader_instance = Tunnel("e5ab36a2e51e:2D")

def convert(stlfile):
    # load stl file
    print("loading stl from file: " + stlfile)
    mesh_obj = stl.mesh.Mesh.from_file(stlfile)
    org_mesh = np.hstack((mesh_obj.v0[:, np.newaxis], mesh_obj.v1[:, np.newaxis], mesh_obj.v2[:, np.newaxis]))
    print("mesh has: ", str(org_mesh.shape))
    vol, scale, shift = stltovoxel.convert_mesh(org_mesh) # vol will be a 3d numpy array
    print("vol has: ", str(vol.shape))
    # convert volume to 3d plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.voxels(vol, edgecolor="k")
    # return figure
    return fig


def convert2d(stlfile, nslice, max_S, xro, yro, zro):
    # load stl file
    print("loading stl from file: " + stlfile)
    mesh_obj = stl.mesh.Mesh.from_file(stlfile)
    org_mesh = np.hstack((mesh_obj.v0[:, np.newaxis], mesh_obj.v1[:, np.newaxis], mesh_obj.v2[:, np.newaxis]))
    print("mesh has: ", str(org_mesh.shape))
    vol, scale, shift = stltovoxel.convert_mesh(org_mesh, resolution=max_S) # vol will be a 3d numpy array
    print("vol has: ", str(vol.shape))
    # rotate volume by xro, yro, zro times
    if xro:
        vol = np.rot90(vol, 1, (0,1))
    if yro:
        vol = np.rot90(vol, 1, (0,2))
    if zro:
        vol = np.rot90(vol, 1, (1,2))    
    # grab a slice at the given z value
    nslice = vol[:,:,nslice]

    # send it to a connected extension
    stlloader_instance.load_data(nslice)

    # return figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(nslice)
    return fig

def save(stlfile, nslice, max_S, xro, yro, zro):
    # load stl file
    print("loading stl from file: " + stlfile)
    mesh_obj = stl.mesh.Mesh.from_file(stlfile)
    org_mesh = np.hstack((mesh_obj.v0[:, np.newaxis], mesh_obj.v1[:, np.newaxis], mesh_obj.v2[:, np.newaxis]))
    print("mesh has: ", str(org_mesh.shape))
    vol, scale, shift = stltovoxel.convert_mesh(org_mesh, resolution=max_S) # vol will be a 3d numpy array
    print("vol has: ", str(vol.shape))
    # rotate volume by xro, yro, zro times
    if xro:
        vol = np.rot90(vol, 1, (0,1))
    if yro:
        vol = np.rot90(vol, 1, (0,2))
    if zro:
        vol = np.rot90(vol, 1, (1,2))    
    # grab a slice at the given z value
    nslice = vol[:,:,nslice]

    # create a simple object
    obj = SimpleObject("stl_slice", nslice)
    # save the object
    return mso.save(obj, tempfile.mktemp(suffix=".mso"))

    
    