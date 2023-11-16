![GitHub last commit](https://img.shields.io/github/last-commit/devbrones/magisim)
![GitHub](https://img.shields.io/github/license/devbrones/magisim)
![GitHub pull requests](https://img.shields.io/github/issues-pr/devbrones/magisim)


<p><img align="right" src="./resources/magisim_logo256.png" width=60></p>
<h1>magisim</h1>

![Magisim project banner](resources/banner1.png)

## Description


Magisim is a versatile simulation hub that brings together individual computational algorithms through an interactive graphical user interface. It is designed to be hosted on a server, allowing multiple users to access it simultaneously. This makes Magisim an affordable and powerful tool for educational environments.

The primary goal of this project is to democratize access to high-cost simulation tools, particularly for electromagnetic and other physical simulations. Magisim is designed for hobbyists, amateurs, and individuals who want to learn about these physical phenomena by visualizing different aspects of simulations.

## Setup

### Conda

Create the conda environment from the `devenv.yml` file:

```bash
conda env create -f devenv.yml
```

Activate the environment:

```bash
conda activate msimdev
```

Install dependencies:

```bash
pip install fdtd
```


### Docker
TODO: add docker instructions

## Usage

### Running the server
Move to the ```src/ui``` directory and run the following command:
```bash
sh start.sh
```
This will start the server on port 8000. You can access the server by navigating to ```localhost:8000``` in your browser. By default the server does not listen from external connections. To allow external connections, edit the config file ```src/ui/shared/config.py``` and change ```Config.UI.listen``` to ```"0.0.0.0"```.


## Documentation

For comprehensive documentation, please visit the [Magisim Documentation](https://magisim.mintlify.app/introduction) on Mintlify.

## Screenshots
### Node Manager
![Screenshot of the built in NodeManager Workflow](resources/nmgr.png)
### Epsilon0 Sim
![Screenshot of Epsilon0 workspace version 0.0.0](resources/fdtd-scrs-v0.0.0.png)

## Features

- Connect and collect computational algorithms.
- Hosted on a server for multi-user access.
- Affordable tool for educational environments.
- Easy-to-use node interface for algorithm composition.
- Visualize simulations, post-process data, and perform analysis.
- SOON: export simulation data to VTK format for visualization in ParaView.
- SOON: openEMS node for FDTD simulations.
- SOON: Epsilon0 node for FDTD simulations.

## Roadmap

[Outline any planned features or improvements for the future.]

## Contributing

We welcome contributions to make Magisim even better. If you'd like to contribute, please review our [Contribution Guidelines](CONTRIBUTING.md).

## Acknowledgments

We would like to express our gratitude to the open-source community for their valuable contributions and inspiration.

## Contact

If you have any questions or need support, feel free to reach out to us via email at [magisim@protonmail.ch](mailto:magisim@protonmail.ch).




---
> **Note**\
> No alpha available, see obsidian vault for notes.



