from platform import machine
from PIL import Image
import numpy as np
import math
import random
import cv2 as cv
import skimage
import skimage.viewer
import csv

Image.MAX_IMAGE_PIXELS = None
image_name1 = input("Enter machine tagged image name with extension: ")
ip_img = Image.open(image_name1) 
imarray1 = np.array(ip_img)
image_name2 = input("Enter manual tagged image name with extension: ")
ip_img = Image.open(image_name2) 
imarray2 = np.array(ip_img)
ip_img.close()
#print(imarray1.shape)
#print(imarray2.shape)
y_axis = imarray1.shape[0] # 680 # size of each section
x_axis = imarray1.shape[1]
total_pixels = x_axis * y_axis
s_size = 70
y_total = math.ceil(y_axis / s_size)
x_total = math.ceil(x_axis / s_size)
yx_total = y_total * x_total

ip_img = []

output_image_name = ''
i = 0
while (i < len(image_name1)):
    if image_name1[i] == '.':
        break
    else:
        output_image_name = output_image_name + image_name1[i]
    i = i + 1
output_image_name = output_image_name + '_comp'

image_o_exten = ''
i = len(image_name1) - 1
while (image_name1[i] != '.'):
    image_o_exten = image_o_exten + image_name1[i]
    i = i - 1
image_o_exten = image_o_exten[::-1]

print("\nDefault color value:")
print('machine tagged value (R,G,B: 0,255,255)')
default_color = input("\nEnter 'y' if you want to use this value: ")
if default_color == 'y':
    r_val_mac = 0
    g_val_mac = 255
    b_val_mac = 255
else:
    r_val_mac = int(input('\nEnter machine tagged value for Red channel: '))
    g_val_mac = int(input('Enter machine tagged value for Green channel: '))
    b_val_mac = int(input('Enter machine tagged value for Blue channel: '))

r_val_man = int(input('\nEnter manually tagged value for Red channel: '))
g_val_man = int(input('Enter manually tagged value for Green channel: '))
b_val_man = int(input('Enter manually tagged value for Blue channel: '))
r_val_int = int(input('\nEnter intersection value for Red channel: '))
g_val_int = int(input('Enter intersection value for Green channel: '))
b_val_int = int(input('Enter intersection value for Blue channel: '))

def fats():
    total_valid_area = 0
    total_manual_area = 0
    total_machine_area = 0
    
    y_i = 0
    while (y_i < y_axis):
        x_i = 0
        while (x_i < x_axis):
            if (imarray1[y_i][x_i][0] == r_val_mac and imarray1[y_i][x_i][1] == g_val_mac and imarray1[y_i][x_i][2] == b_val_mac):
                total_machine_area = total_machine_area + 1
            if (imarray2[y_i][x_i][0] == r_val_man and imarray2[y_i][x_i][1] == g_val_man and imarray2[y_i][x_i][2] == b_val_man):
                total_manual_area = total_manual_area + 1
            x_i = x_i + 1
        y_i = y_i + 1
    
    print('Manually annotated area: ', total_manual_area)  
    print('Machine annotated area: ', total_machine_area)
    print()
    
    y_i = 0
    while (y_i < y_axis):
        x_i = 0
        while (x_i < x_axis):
            if (imarray2[y_i][x_i][0] == r_val_man and imarray2[y_i][x_i][1] == g_val_man and imarray2[y_i][x_i][2] == b_val_man) and (imarray1[y_i][x_i][0] == r_val_mac and imarray1[y_i][x_i][1] == g_val_mac and imarray1[y_i][x_i][2] == b_val_mac):
                imarray1[y_i][x_i][0] = r_val_int
                imarray1[y_i][x_i][1] = g_val_int
                imarray1[y_i][x_i][2] = b_val_int
                total_valid_area = total_valid_area + 1
            elif (imarray2[y_i][x_i][0] == r_val_man and imarray2[y_i][x_i][1] == g_val_man and imarray2[y_i][x_i][2] == b_val_man):
                imarray1[y_i][x_i][0] = r_val_man
                imarray1[y_i][x_i][1] = g_val_man
                imarray1[y_i][x_i][2] = b_val_man
            x_i = x_i + 1
        y_i = y_i + 1    
    
    print('valid area (in pixels):', total_valid_area)
    
    output_accuracy = total_valid_area / (total_valid_area + (total_manual_area - total_valid_area) + (total_machine_area - total_valid_area))
    #print('final values tva, tha, tma: ', total_valid_area, total_manual_area, total_machine_area)
    print('\n\nIoU parameters:')
    print('TP: ', total_valid_area)
    print('FP: ', total_machine_area - total_valid_area)
    print('FN: ', total_manual_area - total_valid_area)
    #output_accuracy = round(output_accuracy * 100, 2)
    print('\nIoU accuracy:', output_accuracy)
    print()

    viewer = skimage.viewer.ImageViewer(imarray1)
    viewer.show()
    data = Image.fromarray(imarray1)
    data.save(output_image_name + '.' + image_o_exten)

fats()