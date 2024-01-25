# shared extension imports
import gradio as gr
from shared.builtin import Extension
from shared.config import Config

# extension specific imports
import extensions.extension_caed19de0a8b.openmsems as ems 

# no imports #


class ExtensionMeta:
	name: str = "MSEMS"
	uuid: str = "20e4e311-43e1-4c3f-af70-caed19de0a8b"
	authors: list = ["devbrones"]
	version: str = "1.1"
	license: str = "LGPL3"
	description: str = """ FDTD Simulator for Magisim """
	# nhr meta
	class ExtensionType:
		types: list = [Extension.Simulator, Extension.Workspace] # list of classes
		layoutCompat: bool = False
		# externalNodes: str = "nodes.js" ## TODO: implement this later so developers can define their own nodes in js!
		hasNodes: [(Extension,(list,list))] = [(Extension.Simulator, ([("Simple object","array2d")],
																	  [("Realtime Plot","matplot"), ("Detector Plot","matplot"), ("Simulation Space", "space")]))]
		hasSettings: bool = True # can be set to be checked by a function later if needed

def load_workspace(app: gr.Blocks):
	with gr.Tab(ExtensionMeta.name, id=ExtensionMeta.uuid):
		gr.Markdown(ExtensionMeta.description)
		with gr.Tab("Space Preparation"):
			# allow the user to change parameters such as grid size, source dimensions, frequency, 
			# object type, position, and lens parameters if the object is a lens
			# allow the user to change the material properties of the object (permittivity)

			with gr.Column():
				with gr.Row():
					with gr.Column():
						#controls here
						gr.Markdown("Add Object")
						with gr.Tabs():
							with gr.Tab("Lens"):
								gr.Markdown("Lens")
								# TODO: Add optional presets for lenses
								with gr.Group("Lens Parameters"):
									gr.Markdown("Lens Parameters")
									# either the user can enter focal length of the lens, and the rest will be calculated.
									# or the user can enter the radius of curvature or the actual mask of the lens.
									# the user can also enter the refractive index of the lens material, which will be used to calculate the permittivity
									# the user can also enter the permittivity directly
									# the user can also choose from a list of common materials (e.g. glass, acrylic, copper, iron, etc.)
									# for now only a biconvex lens is supported
									demolens = gr.Checkbox(label="Enable Lens")
									lens_focal_length = gr.Number(value=0.1, label="Focal Length (mm)")
									lens_radius = gr.Number(value=0.1, label="Radius of Curvature (mm)")
									permittivity = gr.Number(value=1.5 ** 2, label="Permittivity")
									lens_material = gr.Dropdown(label="Material", choices=["Glass", "Acrylic", "Copper", "Iron", "Custom"])
									with gr.Accordion():
										lposxa = gr.Slider(minimum=0, maximum=300, value=30, label="Lens Position X A")
										lposxb = gr.Slider(minimum=0, maximum=300, value=50, label="Lens Position X B")
										lposya = gr.Slider(minimum=0, maximum=300, value=100, label="Lens Position Y A")
										lposyb = gr.Slider(minimum=0, maximum=300, value=99, label="Lens Position Y B")


							with gr.Tab("Upload Object"):
								gr.Markdown("Upload Object")

							with gr.Tab("Simple Object"):
								gr.Markdown("Simple Object")
								use_simple_object = gr.Checkbox(label="Enable Simple Object")
								with gr.Group("Position"):
									gr.Markdown("Position")
									with gr.Row():
										posx = gr.Slider(minimum=0, maximum=300, value=30, label="Position X")
										posy = gr.Slider(minimum=0, maximum=300, value=50, label="Position Y")

					with gr.Column():
						with gr.Tabs():
							with gr.Tab("Grid Preview"):
								gr.Markdown("Grid Preview")
								gp = gr.Plot(label="Grid Preview")
								gpupdate = gr.Button(value="Update", variant="primary")
							with gr.Tab("Draw"):
								gr.Markdown("Draw")
								draw = gr.ImageEditor(label="Draw", type="numpy", width=300, height=300, image_mode="L", )
								drawpreview = gr.Plot(label="Draw Preview")
						with gr.Column():
							with gr.Tabs():
								with gr.Tab("Grid"):
									gr.Markdown("Grid")
									grid_xsize = gr.Slider(minimum=0, maximum=1000, value=300, label="Grid X Size")
									grid_ysize = gr.Slider(minimum=0, maximum=1000, value=300, label="Grid Y Size")
									grid_c = gr.Number(value=299792458, label="Speed of Light (m/s)")
								with gr.Tab("PML"):
									gr.Markdown("PML")
									pml_xlow = gr.Slider(minimum=0, maximum=1000, value=10, label="PML X Low")
									pml_xhigh = gr.Slider(minimum=0, maximum=1000, value=10, label="PML X High")
									pml_ylow = gr.Slider(minimum=0, maximum=1000, value=10, label="PML Y Low")
									pml_yhigh = gr.Slider(minimum=0, maximum=1000, value=10, label="PML Y High")
								with gr.Tab("Source"):
									gr.Markdown("Source")
									with gr.Group("Source Position"):
										gr.Markdown("Source Position")
										with gr.Row():
											source_x = gr.Slider(minimum=0, maximum=1000, value=15, label="X")
											source_y = gr.Slider(minimum=0, maximum=1000, value=50, label="Y")
									with gr.Group("Source Dimensions"):
										gr.Markdown("Source Dimensions")
										with gr.Row():
											source_width = gr.Slider(minimum=0, maximum=1000, value=100, label="Width")
											source_height = gr.Slider(minimum=0, maximum=1000, value=1, label="Height")
									with gr.Group("Source Properties"):
										gr.Markdown("Source Properties")
										gr.Markdown(f"""_Wavelength cheatsheet:_
					 					- e-8 : 1nm (visible light is around 400-700nm)
					 					- e-5 : 1um	(ir)
					 					- e-3 : 1mm (microwave)
					 					- e-2 : 1cm (SHF)
					 					- e-1 : 10cm (UHF)
					 					""")
										with gr.Row():
											wavelength = gr.Number(value=0.0000000635, label="Wavelength (Meters)")
											amplitude = gr.Slider(minimum=0, maximum=100, value=50, label="Amplitude")
											cycles = gr.Slider(minimum=0, maximum=1000, value=100, label="Cycles")
								with gr.Tab("Detector"):
									gr.Markdown("Detector")
									with gr.Group("Detector Position"):
										with gr.Row():
											det_xmin = gr.Slider(minimum=0, maximum=1000, value=80, label="X Min")
											det_xmax = gr.Slider(minimum=0, maximum=1000, value=200, label="X Max")
										with gr.Row():
											det_ymin = gr.Slider(minimum=0, maximum=1000, value=80, label="Y Min")
											det_ymax = gr.Slider(minimum=0, maximum=1000, value=120, label="Y Max")
		
		gpupdate.click(ems.get_grid_preview, inputs=[permittivity, 
											wavelength, 
											amplitude, 
											cycles, 
											lposxa, 
											lposxb, 
											lposya, 
											lposyb, 
											grid_xsize,
											grid_ysize,
											grid_c,
											pml_xlow,
											pml_xhigh,
											pml_ylow,
											pml_yhigh,
											source_x,
											source_y,
											source_width,
											source_height,
											det_xmin,
											det_xmax,
											det_ymin,
											det_ymax,
											draw,
											demolens,
											use_simple_object
											], outputs=[gp])

		with gr.Tab("Simulate"):
			with gr.Column():
				with gr.Row():
					with gr.Column():
						sim = gr.Plot(label="Simulation")
						detplot = gr.Plot(label="Detector Readings")
	
					with gr.Column():						
						timesteps = gr.Slider(minimum=0, maximum=800, value=400, label="Timesteps")
	
						with gr.Accordion("Settings"):
							gr.Markdown(f"""###### Some settings may not be available on your system. **If you are unsure, leave them as they are.**""")
							gr.Markdown(f"""_Not using CUDA may put a lot of stress on your CPU, make sure you have a fire extinguisher nearby._\\ _**note**: CUDA is only available on systems with NVIDIA GPUs_""")
							simsettings_use_cuda = gr.Checkbox(label="Use CUDA", interactive=Config.Compute.CUDA.isAvailable, value=Config.Compute.CUDA.isAvailable)
							gr.Markdown(f"""_Reactive Plots allow you to interact with a simulation. This will ***significantly*** affect performance, but is useful for analysis._""")
							simsettings_reactive_plot = gr.Checkbox(label="Reactive Plot")
							gr.Markdown(f"""_Show detector plot_ **this will significantly lower performance, but is a powerful analysis tool**""")
							simsettings_live_update = gr.Checkbox(label="Live Update Detector readings")
			with gr.Column():
				prbox = gr.Textbox(label="Progress", lines=1)
				with gr.Row():
					stop_btn = gr.Button(value="Stop", variant="stop")
					runsim = gr.Button(value="Run Simulation", variant="primary")
				
				with gr.Accordion(open=False):
					grid_text = gr.Text(label="Grid", lines=20)
	
			
			#update_btn.click(ems.sendtest)
			runsim.click(ems.simulate, inputs=[permittivity, 
									  		simsettings_use_cuda, 
											timesteps, 
											wavelength, 
											amplitude, 
											cycles, 
											simsettings_live_update, 
											lposxa, 
											lposxb, 
											lposya, 
											lposyb, 
											simsettings_reactive_plot,
											grid_xsize,
											grid_ysize,
											grid_c,
											pml_xlow,
											pml_xhigh,
											pml_ylow,
											pml_yhigh,
											source_x,
											source_y,
											source_width,
											source_height,
											det_xmin,
											det_xmax,
											det_ymin,
											det_ymax,
											draw,
											demolens
											], outputs=[sim, grid_text, detplot, prbox])

def save_workspace(app: gr.Blocks):
	pass

