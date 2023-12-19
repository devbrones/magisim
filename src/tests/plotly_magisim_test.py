import gradio as gr


def simulate(lens_permittivity=1.5 ** 2, use_cuda=False, timesteps=400, wavelength=2, amplitude=50, cycles=100, liveupdate=False, lposxa=30, lposxb=50, lposya=100, lposyb=99):
    import os
    import fdtd
    import numpy as np
    import matplotlib.pyplot as plt
    c = 299792458 #m/s
    grid = fdtd.Grid(shape=(300, 300, 1), grid_spacing=0.1 * wavelength) # free air
    if use_cuda:
        print("Using CUDA")
        #fdtd.set_backend("torch.cuda")
    # x boundaries
    grid[0:10, :, :] = fdtd.PML(name="pml_xlow")
    grid[-10:, :, :] = fdtd.PML(name="pml_xhigh")
    # y boundaries
    grid[:, 0:10, :] = fdtd.PML(name="pml_ylow")
    grid[:, -10:, :] = fdtd.PML(name="pml_yhigh")
    simfolder = grid.save_simulation("Lenses")  # initializing environment to save simulation data
    x, y = np.arange(-200, 200, 1), np.arange(190, 200, 1)
    X, Y = np.meshgrid(x, y)
    lens_mask = X ** 2 + Y ** 2 <= 40000
    for j, col in enumerate(lens_mask.T):
        for i, val in enumerate(np.flip(col)):
            if val:
                grid[lposxa + i : lposxb - i, j - lposya : j - lposyb] = fdtd.Object(permittivity=lens_permittivity, name=str(i) + "," + str(j))
                break

    grid[15, 50:150, 0] = fdtd.LineSource(period=wavelength/c, name="source", amplitude=amplitude, cycle=cycles)
    
    # make 3 sources next to each other with the total width of [15, 50:150, 0]
    #grid[15, 50:80, 0] = fdtd.LineSource(period=wavelength/c, name="source1", amplitude=amplitude, cycle=cycles)
    #grid[15, 85:115, 0] = fdtd.LineSource(period=wavelength/c, name="source2", amplitude=amplitude, cycle=cycles)
    #grid[15, 120:150, 0] = fdtd.LineSource(period=wavelength/c, name="source3", amplitude=amplitude, cycle=cycles)



    #grid[80:200, 80:120, 0] = fdtd.BlockDetector(name="detector")
    grid[224:225, 25:175, 0] = fdtd.BlockDetector(name="detector2")

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



    for i in range(timesteps):
        grid.step()  # running simulation 1 timestep a time and animating
        if i % 10 == 0:
            # saving frames during visualization
            # grid.visualize(z=0, animate=True, index=i, save=True, folder=simfolder)
            #  live update plot from simulation
            if liveupdate:
                grid.save_data()  # saving detector readings
                df = np.load(os.path.join(simfolder, "detector_readings.npz"))
                yield gr.Plot(grid.visualize(z=0, show=False, index=i, cmap="turbo", objcolor=(1,1,1,0.1), srccolor="white", save=False, plotly=True)), str('\n'.join(descript_object)), fdtd.dB_map_2D(df["detector2 (E)"], ret_plot=True)
            else:
                yield gr.Plot(grid.visualize(z=0, show=False, index=i, cmap="turbo", objcolor=(1,1,1,0.1), srccolor="white", save=False, plotly=True)), str('\n'.join(descript_object)), None
            #plt.title(f"{i:3.0f}")



# set up gradio app
            
def load_ui(app: gr.Blocks):

    # lets make a gradio interface
    gr.Markdown("Plotly live update test")
    plot = gr.Plot(label="Plot")
    plot2 = gr.Plot(label="Plot2")
    etctest = gr.Textbox(lines=10, label="etc")
    startbtn = gr.Button("Start")
    startbtn.click(simulate, None, [plot, etctest, plot2])





with gr.Blocks() as app:
    load_ui(app)


app.launch()