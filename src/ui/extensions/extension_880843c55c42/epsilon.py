import fdtd
import numpy as np
import fdtd.backend as bd
import matplotlib.pyplot as plt
from shared.builtin import Extension

# import these in later versions
# import altair as alt
# import pandas as pd
# import plotly.express as px # plotly is a bit more complicated to use, but it has some nice features
# from vega_datasets import data 
# from vtk.util import numpy_support
# import vtk

# code snippet for smith chart using plotly
# import plotly.graph_objects as go
# fig = go.Figure(go.Scattersmith(imag=[0.5, 1, 2, 3], real=[0.5, 1, 2, 3]))
# fig.show()



class Simulator(Extension.Simulator):
    # it is common practice to have the main extension simulator class inherit from the Extension.Simulator class. Same goes for the other extension types
    FDTD = fdtd
    def run(sim, amp , freq, space, xpos, ypos) -> list:
        # assume 2d sim space for now, lets add a switch for 3d later

        # set variables
        # calculate period from frequency
        period = 1/freq
        # set permittivity and permeability (vacuum)
        permittivity = 1.0
        permeability = 1.0
        # set courant number
        courant_number = None
        # set grid spacing
        grid_spacing = 155e-9
        # set grid shape
        grid_shape = (25e-6, 25e-6, 1)
        # create FDTD Grid
        grid = fdtd.Grid(
            shape = grid_shape, 
            grid_spacing = grid_spacing, 
            permittivity = permittivity, 
            permeability = permeability, 
            courant_number = courant_number
            )
        
        # signature
        grid[7.5e-6:8.0e-6, 11.8e-6:13.0e-6, 0] = fdtd.LineSource(
            period = period, # timesteps or seconds
            amplitude = amp,
            phase_shift = 0.0,
            name = "source",
        )

        # x boundaries
        grid[0:10, :, :] = fdtd.PML(name="pml_xlow")
        grid[-10:, :, :] = fdtd.PML(name="pml_xhigh")

        # y boundaries
        grid[:, 0:10, :] = fdtd.PML(name="pml_ylow")
        grid[:, -10:, :] = fdtd.PML(name="pml_yhigh")

        print(grid)
        grid.run(total_time=100)
        grid.visualize(z=0)
        fig, axes = plt.subplots(2, 3, squeeze=False)
        titles = ["Ex: xy", "Ey: xy", "Ez: xy", "Hx: xy", "Hy: xy", "Hz: xy"]

        fields = bd.stack(
            [
                grid.E[:, :, 0, 0],
                grid.E[:, :, 0, 1],
                grid.E[:, :, 0, 2],
                grid.H[:, :, 0, 0],
                grid.H[:, :, 0, 1],
                grid.H[:, :, 0, 2],
            ]
        )

        m = max(abs(fields.min().item()), abs(fields.max().item()))

        for ax, field, title in zip(axes.ravel(), fields, titles):
            ax.set_axis_off()
            ax.set_title(title)
            ax.imshow(bd.numpy(field), vmin=-m, vmax=m, cmap="RdBu")

        return plt

