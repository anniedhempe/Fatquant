from PIL import Image
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math

Image.MAX_IMAGE_PIXELS = None
image1 = input('Enter image name with extension: ')
#im = Image.open('shot7.tif')
im = Image.open(image1)
#im.show()

imarray = np.array(im)
print(imarray.shape, imarray.size, len(imarray))

threshold1 = input('Enter threshold value: ')
threshold1 = int(threshold1)

i1 = 0
while (i1 < len(imarray)):
    i2 = 0
    while (i2 < len(imarray[i1])):
        #print((imarray[i1][i2][0] + imarray[i1][i2][1] + imarray[i1][i2][2]) / 3)
        val_i = int(imarray[i1][i2][0]) 
        val_i = val_i + int(imarray[i1][i2][1])
        val_i = val_i + int(imarray[i1][i2][2])
        val_i = int(val_i / 3)
        if val_i < threshold1:
            imarray[i1][i2][0] = int(0)
            imarray[i1][i2][1] = int(0)
            imarray[i1][i2][2] = int(0)
        else:
            imarray[i1][i2][0] = int(255)
            imarray[i1][i2][1] = int(255)
            imarray[i1][i2][2] = int(255)
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
#data.save('E:/Annie Madam/Biology/Pancreas/liver_images/non-fatty/thresholded_samples/' + str(image1_name))
#data.save('shot7_bi2.tif')