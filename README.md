# Deep learning mask segmentation based on Rembg

Program developed to generate mask images of objects like rock samples and other similar objects photographed in green static background for photogrammetry reconstruction. The script encapsulated in a QT interface uses the Rembg library (based on the U2net architecture) to predict the masks from a folder chosen by the user. The script saves the predicted masks adding "_mask.png", which is the standard for Agisoft Metashape masks.


## Usage
 
 To run this program use:
 
    python generate_MASKS_rembg.py
  
Choose the input folder with original images in jpeg format, and choose and or create the output folder where the masks will be saved. Hit "Process masks" to start the mask generation.

<img src="https://github.com/ademirmarquesjunior/mask_segmentation_rembg/blob/main/images/usage.png" width="600" alt="Segmented image">



## Requirements

- [Rembg](https://github.com/danielgatis/rembg)
- Numpy
- Pillow
- Glob
- Sys
- PyQT5


## Install

To install this software/script download and unpack the software package in any folder.

Install the required libraries individually or run the script bellow:
 
     pip install -r Requirements.txt


## Credits	
This work is credited to the [Vizlab | X-Reality and GeoInformatics Lab](http://vizlab.unisinos.br/) and the following developers:	[Ademir Marques Junior](https://www.researchgate.net/profile/Ademir_Junior) and [Gustavo Correia de Almeida](https://github.com/pavaonegro/).

## License

    MIT Licence (https://mit-license.org/)
    
## How to cite

Yet to be published.
