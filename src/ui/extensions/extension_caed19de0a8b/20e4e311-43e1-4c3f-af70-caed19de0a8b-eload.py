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
	version: str = "0.0.0"
	license: str = "LGPL3"
	description: str = """ FDTD Simulator for Magisim """
	# nhr meta
	class ExtensionType:
		types: list = [Extension.Simulator, Extension.Workspace] # list of classes
		layoutCompat: bool = False
		# externalNodes: str = "nodes.js" ## TODO: implement this later so developers can define their own nodes in js!
		hasNodes: [(Extension,(list,list))] = [(Extension.Simulator, ([("Source Position X","number"),
																       ("Source Position Y","number"), 
																	   ("Wavelength","number"),
																	   ("Frequency","number"),
																	   ("Phase","number"),
																	   ("Amplitude (dB)","number"),
																	   ("Domain","np2d"),
																	   ("Object","np2d"),
																	   ("Simple Object","np2d"),
                                                                       ("PML","np2d")],
																	  [("Frequency Domain","np2d"),
					                                                   ("Time Domain","np2d"),
																	   ("E","np2d"),
																	   ("H","np2d")])),
																	   (Extension.Editor, ([("Sim Space","np2d")],[("Domain","np2d"), ("Object","np2d"), ("PML","np2d")]))]
		hasSettings: bool = True # can be set to be checked by a function later if needed

def load_workspace(app: gr.Blocks):
	with gr.Tab(ExtensionMeta.name):
		gr.Markdown(ExtensionMeta.description)
		with gr.Column():
			with gr.Row():
				with gr.Column():
					sim = gr.Plot(label="Simulation")
					space = gr.Plot(label="Space")

				with gr.Column():
					simpleObjectEpsilon = gr.Slider(minimum=0, maximum=50, value=2, label="Simple Object Permittivity")
					gr.Markdown(f"""_Wavelength cheatsheet:_
				 					- e-8 : 1nm (visible light is around 400-700nm)
				 					- e-5 : 1um	(ir)
				 					- e-3 : 1mm (microwave)
				 					- e-2 : 1cm (SHF)
				 					- e-1 : 10cm (UHF)
				 		""")
					wavelength = gr.Number(value=0.0000000635, label="Wavelength (Meters)")
					timesteps = gr.Slider(minimum=0, maximum=800, value=400, label="Timesteps")
					amplitude = gr.Slider(minimum=0, maximum=100, value=50, label="Amplitude")
					cycles = gr.Slider(minimum=0, maximum=1000, value=100, label="Cycles")
					lposxa = gr.Slider(minimum=0, maximum=300, value=30, label="Lens Position X A")
					lposxb = gr.Slider(minimum=0, maximum=300, value=50, label="Lens Position X B")
					lposya = gr.Slider(minimum=0, maximum=300, value=100, label="Lens Position Y A")
					lposyb = gr.Slider(minimum=0, maximum=300, value=99, label="Lens Position Y B")

					with gr.Accordion("Settings"):
						gr.Markdown(f"""###### Some settings may not be available on your system. **If you are unsure, leave them as they are.**""")
						gr.Markdown(f"""_Not using CUDA may put a lot of stress on your CPU, make sure you have a fire extinguisher nearby._""")
						simsettings_use_cuda = gr.Checkbox(label="Use CUDA", interactive=Config.Compute.CUDA.isAvailable, value=Config.Compute.CUDA.isAvailable)
						gr.Markdown(f"""_Reactive Plots allow you to interact with a simulation while it is running. this is not reccomended as it will significantly affect simulation speeds_""")
						simsettings_reactive_plot = gr.Checkbox(label="Reactive Plot", interactive=False)
						gr.Markdown(f"""_Object specific settings. If you are unsure, it is reccomended to not change these._""")
						options = gr.CheckboxGroup(["Simple Object"], label="Object")
						gr.Markdown(f"""_Live update detector plot_ **this will significantly lower performance, but may give a better overview**""")
						simsettings_live_update = gr.Checkbox(label="Live Update Detector readings")
		with gr.Column():
			with gr.Row():
				update_btn = gr.Button(value="Update", variant="primary")
				runsim = gr.Button(value="Run Simulation", variant="secondary")
			
			with gr.Accordion(open=False):
				grid_text = gr.Code(label="Grid", lines=20)

		
		update_btn.click(ems.sendtest)
		runsim.click(ems.simulate, inputs=[simpleObjectEpsilon, simsettings_use_cuda, timesteps, wavelength, amplitude, cycles, simsettings_live_update, lposxa, lposxb, lposya, lposyb], outputs=[sim, grid_text, space])

