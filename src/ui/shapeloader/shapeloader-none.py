import numpy as np
import matplotlib.pyplot as plt



class ShapeLoader:

    def create(input_file, modeselector=None, res=None, cutpoint=None, xpos=0, ypos=0, output_xyz_file=None):
        ##
        ## Determine if the input is 3d or 2d and then generate the appropriate numpy arrays
        ##

        # 3D
        ff3d = ["obj", "ply", "step"]
        if any(x in input_file.name.split(".")[-1] for x in ff3d):
            ff = input_file.name.split(".")[-1]
            if ff == ff3d[0]:
                ## load as obj
                

class filetest:
    name = "test.obj"

ShapeLoader.create(filetest)
            