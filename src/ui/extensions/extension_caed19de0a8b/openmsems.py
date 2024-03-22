from shared.router import Router, Tunnel
import gradio as gr
import pickle
from tqdm import tqdm
from shared.libmso import mso, SimpleObject
import fdtd
import numpy as np
import matplotlib.pyplot as plt

# Instantiate your extension with the given UUID
openmsems_simpleobject = Tunnel("caed19de0a8b:Simple object")

def get_simple_object():
    return openmsems_simpleobject.receive_data()


def get_grid_preview(mso_file=None,
                        lens_permittivity=1.5 ** 2,
                        wavelength=2,
                        amplitude=50,
                        cycles=100,
                        lposxa=30,
                        lposxb=50,
                        lposya=100,
                        lposyb=99,
                        grid_xsize=300,
                        grid_ysize=300,
                        grid_c=299792458,
                        pml_xlow=10,
                        pml_xhigh=10,
                        pml_ylow=10,
                        pml_yhigh=10,
                        src_type="Line",
                        src_ct=1,
                        src_x=15,
                        src_y=50,
                        src_width=100,
                        src_height=1,
                        det_xmin=0,
                        det_xmax=0,
                        det_ymin=0,
                        det_ymax=0,
                        use_det=False,
                        draw=None,
                        demolens=False,
                        use_simple_object=False,
                        cache_object=True,
                        sposx=0,
                        sposy=0
                        ):
    print(src_type)
    c = grid_c #m/s
    grid = fdtd.Grid(shape=(grid_xsize, grid_ysize, 1), grid_spacing=0.1 * wavelength) # free air
    # x boundaries
    grid[0:pml_xlow, :, :] = fdtd.PML(name="pml_xlow")
    grid[-pml_xhigh:, :, :] = fdtd.PML(name="pml_xhigh")
    # y boundaries
    grid[:, 0:pml_ylow, :] = fdtd.PML(name="pml_ylow")
    grid[:, -pml_yhigh:, :] = fdtd.PML(name="pml_yhigh")

    if mso_file is not None and not use_simple_object:
        # read the mso file and add it to the grid
        simpleobject = mso.read(mso_file)
        if not isinstance(simpleobject, SimpleObject):
            raise ValueError("The file is not a valid SimpleObject")
        # add the simple object to the grid at the specified position, where the x and y are the top left corner of the object it is a 2d array
        for i in tqdm.tqdm(range(simpleobject.data.shape[0])):
            for j in range(simpleobject.data.shape[1]):
                #grid[sposx + i, sposy + j, 0] = fdtd.Object(permittivity=simpleobject[i, j], name=f"{i}---{j}")
                # check if the point is existing
                if simpleobject.data[i, j]:
                    grid[sposx + i, sposy + j, 0] = fdtd.Object(permittivity=lens_permittivity, name=f"{i}---{j}")

    if use_simple_object and mso_file is None:
        simpleobject = openmsems_simpleobject.receive_data()["pickle_jar"]
        # add the simple object to the grid at the specified position, where the x and y are the top left corner of the object it is a 2d array
        for i in tqdm.tqdm(range(simpleobject.shape[0])):
            for j in range(simpleobject.shape[1]):
                #grid[sposx + i, sposy + j, 0] = fdtd.Object(permittivity=simpleobject[i, j], name=f"{i}---{j}")
                # check if the point is existing
                if simpleobject[i, j]:
                    grid[sposx + i, sposy + j, 0] = fdtd.Object(permittivity=lens_permittivity, name=f"{i}---{j}")
                
        
        

    if demolens:
        print("demolens")
        x, y = np.arange(-200, 200, 1), np.arange(190, 200, 1)
        X, Y = np.meshgrid(x, y)
        lens_mask = X ** 2 + Y ** 2 <= 40000
        for j, col in enumerate(lens_mask.T):
            for i, val in enumerate(np.flip(col)):
                if val:
                    grid[lposxa + i : lposxb - i, j - lposya : j - lposyb] = fdtd.Object(permittivity=lens_permittivity, name=str(i) + "," + str(j))
                    break
    
    # add the drawn object to the grid
    #if draw is not None:
    #    print("draw is not none")
    #    #image should be a numpy array of shape (grid_xsize, grid_ysize, 3) with values between 0 and 255, 
    #    #we need to convert it to a boolean array of shape (grid_xsize, grid_ysize), since we are using monochrome mode
    #    #we can just take the first channel only
    #    print(draw['composite'].shape)
    #    draw = draw['composite'].astype(bool)
    #    #iterate over the grid and create a object with the name as the coordinates
    #    for i in range(grid_xsize):
    #        for j in range(grid_ysize):
    #            if draw[i,j]:
    #                grid[i,j] = fdtd.Object(permittivity=1.5**2, name=f"{i}---{j}")

    if src_type == "Line":
        # calculate the appropriate source dimensions as a slice from the values
        #grid[15, 50:150, 0] = fdtd.LineSource(period=wavelength/c, name="source", amplitude=amplitude, cycle=cycles)
        grid[src_x, src_y:src_y+src_width, 0] = fdtd.LineSource(period=wavelength/c, name="source", amplitude=amplitude, cycle=cycles)
        print("calculated source dimensions")
        # make 3 sources next to each other with the total width of [15, 50:150, 0]
        #grid[15, 50:80, 0] = fdtd.LineSource(period=wavelength/c, name="source1", amplitude=amplitude, cycle=cycles)
        #grid[15, 85:115, 0] = fdtd.LineSource(period=wavelength/c, name="source2", amplitude=amplitude, cycle=cycles)
        #grid[15, 120:150, 0] = fdtd.LineSource(period=wavelength/c, name="source3", amplitude=amplitude, cycl2e=cycles)
    elif src_type == "Point":
        grid[src_x, src_y, 0] = fdtd.PointSource(period=wavelength/c, name="source", amplitude=amplitude, cycle=cycles)
        print("calculated source dimensions")
    elif src_type == "Points":
        # add as many points as specified by src_ct in a line of the width selected by src_width evenly spaced
        for i in range(src_ct):
            grid[src_x, src_y + i * src_width // src_ct, 0] = fdtd.PointSource(period=wavelength/c, name=f"source{i}", amplitude=amplitude, cycle=cycles)
        print("calculated source dimensions")



    if use_det:
        grid[det_xmin:det_xmax, det_ymin:det_ymax, 0] = fdtd.BlockDetector(name="detector")
        print("added detector")
    #grid[224:225, 25:175, 0] = fdtd.BlockDetector(name="detector2")
    # create a detector that spans the entire grid
    #grid[0:299, 0:299, 0] = fdtd.BlockDetector(name="detector2") # enormous yikes

    descript_object = []
    descript_object.append(str(grid))
    #wavelength = 3e8/grid.source.frequency
    #wavelengthUnits = wavelength/grid.grid_spacing
    GD = np.array([grid.x, grid.y, grid.z])
    gridRange = [np.arange(x/grid.grid_spacing) for x in GD]
    objectRange = np.array([[gridRange[0][x.x], gridRange[1][x.y], gridRange[2][x.z]] for x in grid.objects], dtype=object).T
    descript_object.append("\n\nGrid details (in wavelength scale):")
    descript_object.append("\n\tGrid dimensions: ")
    descript_object.append(str(GD/wavelength))
    descript_object.append("\n\tSource dimensions: ")
    #descript_object.append(str(np.array([grid.source.x[-1] - grid.source.x[0] + 1, grid.source.y[-1] - grid.source.y[0] + 1, grid.source.z[-1] - grid.source.z[0] + 1])/wavelengthUnits))
    descript_object.append("\n\tObject dimensions: ")
    #descript_object.append(str([(max(map(max, x)) - min(map(min, x)) + 1)/wavelengthUnits for x in objectRange]))
    print("created description object")

    # we don't need to run the simulation, just return the grid
    print("returning grid")
    return gr.Plot(grid.visualize(z=0, show=False, plotly=False, index=0, cmap="turbo", objcolor=(1,1,1,0.1), srccolor="white", save=False))
    


def simulate(mso_file=None,
             lens_permittivity=1.5 ** 2, 
             use_cuda=False, 
             timesteps=400, 
             wavelength=2, 
             amplitude=50, 
             cycles=100, 
             liveupdate=False, 
             lposxa=30, 
             lposxb=50, 
             lposya=100, 
             lposyb=99, 
             reactive=False,
             grid_xsize=300,
             grid_ysize=300,
             grid_c=299792458,
             pml_xlow=10,
             pml_xhigh=10,
             pml_ylow=10,
             pml_yhigh=10,
             src_type="Line",
             src_ct=1,
             src_x=15,
             src_y=50,
             src_width=100,
             src_height=1,
             det_xmin=0,
             det_xmax=0,
             det_ymin=0,
             det_ymax=0,
             use_det=False,
             draw=None,
             demolens=False,
             use_simple_object=False,
             cache_object=True,
             sposx=0,
             sposy=0
             ):

    c = grid_c #m/s

    grid = fdtd.Grid(shape=(grid_xsize, grid_ysize, 1), grid_spacing=0.1 * wavelength) # free air

    # set the backend to numpy or torch
    fdtd.set_backend("numpy")
    if use_cuda:
        print("Using CUDA")
        fdtd.set_backend("torch")
    
    # x boundaries
    grid[0:pml_xlow, :, :] = fdtd.PML(name="pml_xlow")
    grid[-pml_xhigh:, :, :] = fdtd.PML(name="pml_xhigh")
    # y boundaries
    grid[:, 0:pml_ylow, :] = fdtd.PML(name="pml_ylow")
    grid[:, -pml_yhigh:, :] = fdtd.PML(name="pml_yhigh")

    #
    # Check if we are using a simple object and add it to the grid
    # 
    if mso_file is not None and not use_simple_object:
        # read the mso file and add it to the grid
        simpleobject = mso.read(mso_file)
        if not isinstance(simpleobject, SimpleObject):
            raise ValueError("The file is not a valid SimpleObject")
        # add the simple object to the grid at the specified position, where the x and y are the top left corner of the object it is a 2d array
        for i in tqdm.tqdm(range(simpleobject.data.shape[0])):
            for j in range(simpleobject.data.shape[1]):
                #grid[sposx + i, sposy + j, 0] = fdtd.Object(permittivity=simpleobject[i, j], name=f"{i}---{j}")
                # check if the point is existing
                if simpleobject.data[i, j]:
                    grid[sposx + i, sposy + j, 0] = fdtd.Object(permittivity=lens_permittivity, name=f"{i}---{j}")

    #
    # Check if we are using a simple object that is being sent from a node and add it to the grid
    # 
    if use_simple_object and mso_file is None:
        simpleobject = openmsems_simpleobject.receive_data()["pickle_jar"]
        # add the simple object to the grid at the specified position, where the x and y are the top left corner of the object it is a 2d array
        for i in tqdm.tqdm(range(simpleobject.shape[0])):
            for j in range(simpleobject.shape[1]):
                #grid[sposx + i, sposy + j, 0] = fdtd.Object(permittivity=simpleobject[i, j], name=f"{i}---{j}")
                # check if the point is existing
                if simpleobject[i, j]:
                    grid[sposx + i, sposy + j, 0] = fdtd.Object(permittivity=lens_permittivity, name=f"{i}---{j}")
    
    #
    # Check if we are using a example lens object and add it to the grid
    #
    if demolens:
        x, y = np.arange(-200, 200, 1), np.arange(190, 200, 1)
        X, Y = np.meshgrid(x, y)
        lens_mask = X ** 2 + Y ** 2 <= 40000
        for j, col in enumerate(lens_mask.T):
            for i, val in enumerate(np.flip(col)):
                if val:
                    grid[lposxa + i : lposxb - i, j - lposya : j - lposyb] = fdtd.Object(permittivity=lens_permittivity, name=str(i) + "," + str(j))
                    break

    #
    # add the drawn object to the grid
    #
    """if draw is not None:
        #image should be a numpy array of shape (grid_xsize, grid_ysize, 3) with values between 0 and 255, 
        #we need to convert it to a boolean array of shape (grid_xsize, grid_ysize), since we are using monochrome mode
        #we can just take the first channel only
        print(draw['composite'].shape)
        draw = draw['composite'].astype(bool)
        #iterate over the grid and create a object with the name as the coordinates
        for i in range(grid_xsize-1):
            for j in range(grid_ysize-1):
                if draw[i,j]:
                    grid[i,j] = fdtd.Object(permittivity=1.5**2, name=f"{i}---{j}")
    """
    #
    # Determine source type and add them to the grid
    #
    if src_type == "Line":
        # calculate the appropriate source dimensions as a slice from the values
        grid[src_x, src_y:src_y+src_width, 0] = fdtd.LineSource(period=wavelength/c, name="source", amplitude=amplitude, cycle=cycles)
        print("calculated source dimensions")
    elif src_type == "Point":
        # add a single point source to the grid
        grid[src_x, src_y, 0] = fdtd.PointSource(period=wavelength/c, name="source", amplitude=amplitude, cycle=cycles)
        print("calculated source dimensions")
    elif src_type == "Points":
        # add as many points as specified by src_ct in a line of the width selected by src_width evenly spaced
        for i in range(src_ct):
            grid[src_x, src_y + i * src_width // src_ct, 0] = fdtd.PointSource(period=wavelength/c, name=f"source{i}", amplitude=amplitude, cycle=cycles)
        print("calculated source dimensions")

    descript_object = []
    descript_object.append(str(grid))
    #wavelength = 3e8/grid.source.frequency
    #wavelengthUnits = wavelength/grid.grid_spacing
    GD = np.array([grid.x, grid.y, grid.z])
    gridRange = [np.arange(x/grid.grid_spacing) for x in GD]
    objectRange = np.array([[gridRange[0][x.x], gridRange[1][x.y], gridRange[2][x.z]] for x in grid.objects], dtype=object).T
    descript_object.append("\n\nGrid details (in wavelength scale):")
    descript_object.append("\n\tGrid dimensions: ")
    descript_object.append(str(GD/wavelength))
    descript_object.append("\n\tSource dimensions: ")
    #descript_object.append(str(np.array([grid.source.x[-1] - grid.source.x[0] + 1, grid.source.y[-1] - grid.source.y[0] + 1, grid.source.z[-1] - grid.source.z[0] + 1])/wavelengthUnits))
    descript_object.append("\n\tObject dimensions: ")
    #descript_object.append(str([(max(map(max, x)) - min(map(min, x)) + 1)/wavelengthUnits for x in objectRange]))
    print("GRID DETS:")
    #for obj in (grid.E, grid.H):
    #    print(obj)

    for i in tqdm(range(timesteps)):
        grid.step()  # running simulation 1 timestep a time and animating
        if i % 10 == 0:
            if liveupdate:
                yield gr.Plot(grid.visualize(z=0, show=False, plotly=reactive, index=i, cmap="turbo", objcolor=(1,1,1,0.1), srccolor="white", save=False)), str('\n'.join(descript_object)), fdtd.dB_map_2D(grid.detectors[0], show=False, plotly=True)
            else:
                yield gr.Plot(grid.visualize(z=0, show=False, plotly=reactive, index=i, cmap="turbo", objcolor=(1,1,1,0.1), srccolor="white", save=False)), str('\n'.join(descript_object)), None
            plt.title(f"{i:3.0f}")

