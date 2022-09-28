# Fatquant
 An automated image analysis tool for quantification of fat cells

![alt text](Fatquant_readme_display.png)

This tool was designed for the experiment mentioned in:
[https://www.biorxiv.org/content/10.1101/2021.12.13.472341v1]

### Requirements
* Python 3 distribution: Anaconda
* Other needed package name(s): pillow 

## Tutorial
(A raw image `Figure_28.png` and its fat tagged version `Figure_28_tagged.png` from the directiory **Small_samples** will be referred to demonstrate fat analysis)

1) Once this repository is downloaded in your local machine, open the Fatquant folder using an IDE that supports Python 3 (e.g. Visual Studio Code).
2) Run the file named `tool_dos.py` under an interpreter of Anaconda and execute options from the menu as per requirements.

#### Option 1
This option allows binary thresholding to be performed on either a raw image or a tagged image in each attempt.

For raw image, you can refer the following inputs:

`Enter threshold value: Small_samples/Figure_28.png`

`Enter threshold value: 228`

For image with manual tagged fats, you can refer the following inputs:

`Enter image name with extension: Small_samples/Figure_28_tagged.png`

`Enter 'y' if you want to use default manually tagged color value (R,G,B: 255,255,0): n`

`Enter value for Red channel: 255`

`Enter value for Green channel: 255`

`Enter value for Blue channel: 0`

(For this image, default color option would have given the output but manual entry of color was chosen to demonstrate what values to enter)

#### Option 2
This option allows segmentation of white pixels to be performed on binary thresholded raw image or manually tagged image.

For raw image, you can refer the following inputs:

`Enter thresholded image name with extension: Small_samples/Figure_28_228.png`

`Enter 'y' if the thresholded image is of manually tagged data: n`

For image with manual tagged fats, you can refer the following inputs:

`Enter thresholded image name with extension: Small_samples/Figure_28_tagged_bi.png

Enter 'y' if the thresholded image is of manually tagged data: y`
