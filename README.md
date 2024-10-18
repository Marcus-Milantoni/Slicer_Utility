# slicerutil
A package containing usefull functions for working with common nodes in 3D Slicer as NumPyArrays. 

## Table of Contents
- [Usage](#Usage)
- [License](#License)
- [Requirements](#Requirements)
- [Setup](#Setup)
- [Tutorial](#Description)
- [Example patients](#Examples)
- [Acknowledgements](#Acknowledgements)

## Usage
!!!!Please install this package in a Slicer python environment!!!!

_After installing the package use the following to import_ <br>

**import slicerutil as su**

<br>

## License
The following repository is under MIT license.

## Setup

### Downloading the 3D slicer application & supporting software

Please follow the steps provided bellow:
1. Visit [slicer](https://download.slicer.org) to download the application.
2. Visit [anaconda](https://www.anaconda.com/download) to download python3/ jupyter notebook.
3. Visit [Visual Studio Code](https://code.visualstudio.com/Download) to download the source-code editor (optional).
4. From the Extensions Manager widget, download the SlicerJupyter, MeshToLabelMap, PETDICOMExtension (if working with PET DICOMS), SlicerRT (if working with radiotherapy data).
    - The Slicer application needs to restart to install the extensions.

### Set up the SlicerJupyter

1. Using the search widget in Slicer, open the SlicerJupyter extension by searching for JupyterKernel.
2. Click the "Start Jupyter Server" button. A JupyterLab notebook will open when the setup is complete.
3. Click the "Jupyter server in external Python environment" and copy the command to clipboard.
4. Open the anaconda prompt (Terminal if on mac) and paste the command.
5. (Optional) open an external environment (Visual Studio Code) and select the Slicer kernel!


## Acknowledgements
The slicer scripting tutorial would not be possible without the following open source software:
- [Slicer](https://github.com/Slicer/Slicer)
- [Numpy](https://github.com/numpy/numpy)
- [Matplotlib](https://github.com/matplotlib/matplotlib)
