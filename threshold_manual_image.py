from PIL import Image
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math

image1 = input('Enter image name with extension: ')
#im = Image.open('shot7.tif')
im = Image.open(image1)
#im = Image.open('E:/Annie Madam/Biology/Pancreas/liver_images/non-fatty/samples/' + str(image1))
#im = Image.open('GTEX-1117F-1726 (1).svs')
#im.show()

imarray = np.array(im)
print(imarray.shape, imarray.size, len(imarray))

clr_resp = input("Press 'y' for default manual color value (R,G,B: 255,255,0): ") # User color response
if clr_resp != 'y':
    r_val = int(input('Enter value for Red channel: '))
    g_val = int(input('Enter value for Green channel: '))
    b_val = int(input('Enter value for Blue channel: '))
    i1 = 0
    while (i1 < len(imarray)):
        i2 = 0
        while (i2 < len(imarray[i1])):
            if imarray[i1][i2][0] == r_val and imarray[i1][i2][1] == g_val and imarray[i1][i2][2] == b_val:
                imarray[i1][i2][0] = int(255)
                imarray[i1][i2][1] = int(255)
                imarray[i1][i2][2] = int(255)
            else:
                imarray[i1][i2][0] = int(0)
                imarray[i1][i2][1] = int(0)
                imarray[i1][i2][2] = int(0)
            i2 = i2 + 1
        i1 = i1 + 1
else:
    i1 = 0
    while (i1 < len(imarray)):
        i2 = 0
        while (i2 < len(imarray[i1])):
            if imarray[i1][i2][0] == 255 and imarray[i1][i2][1] == 255 and imarray[i1][i2][2] == 0:
                imarray[i1][i2][0] = int(255)
                imarray[i1][i2][1] = int(255)
                imarray[i1][i2][2] = int(255)
            else:
                imarray[i1][i2][0] = int(0)
                imarray[i1][i2][1] = int(0)
                imarray[i1][i2][2] = int(0)
            i2 = i2 + 1
        i1 = i1 + 1

data = Image.fromarray(imarray)
print('Done')
image1_name = ''
image1_exten = ''

i = len(image1) - 1
while (image1[i] != '.'):
    image1_exten = image1_exten + image1[i]
    i = i - 1
image1_exten = image1_exten[::-1]

i = len(image1) - len(image1_exten) - 1 # (-1 for '.')
i = i - 1 # since range = 0 -> length - 1
while (i >= 0):
    image1_name = image1_name + image1[i]
    i = i - 1
image1_name = image1_name[::-1]
image1_name = image1_name + '_bi.' + image1_exten
data.save(image1_name)
#data.save('shot7_bi2.tif')