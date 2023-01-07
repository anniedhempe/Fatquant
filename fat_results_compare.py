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

img_grid = []
img_grid_man = []
for i in range(total_pixels):
    img_grid.append([])
    img_grid_man.append([])

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

group_names = input("Enter 'y' for default white group names: ")
if group_names == 'y':
    combined_file = open('white_groups_combined_manual.csv', 'r', newline='', encoding='utf16')
    csv_reader1 = csv.reader(combined_file)
    segmented_file = open('white_groups_segmented_manual.csv', 'r', newline='', encoding='utf16')
    csv_reader2 = csv.reader(segmented_file)
else:
    combined_name = input("Enter file name for manually tagged white groups combined (extension 'csv'): ")
    segmented_name = input("Enter file name for manually tagged white groups segmented (extension 'csv'): ")
    combined_file = open(combined_name, 'r', newline='', encoding='utf16')
    csv_reader1 = csv.reader(combined_file)
    segmented_file = open(segmented_name, 'r', newline='', encoding='utf16')
    csv_reader2 = csv.reader(segmented_file)

# File referred to identify value of total machine tagged fat area
file_name = input("\nEnter file name for machine tagged fat areas (extension 'csv'): ")
file_file = open(file_name, 'r', newline='', encoding='utf16')
csv_reader3 = csv.reader(file_file)

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
    
combined_dataset_man = [[[]]]
segmented_dataset_man = []
fat_areas_mac = []

i = 0
i1 = -1
for line in csv_reader1:
    if len(line) == 0:
        combined_dataset_man.append([])
        i = i + 1
        i1 = -1
    else:
        if len(line) == 3:
            combined_dataset_man[i][i1].append([int(line[0]), int(line[1]), int(line[2])])
        elif len(line) == 2:
            combined_dataset_man[i].append([])
            i1 = i1 + 1
            combined_dataset_man[i][i1].append([int(line[0]), int(line[1])])
i = 0 # remove null lists
while (i < len(combined_dataset_man)):
    if len(combined_dataset_man[i]) == 0:
        del combined_dataset_man[i]
    else:
        i1 = 0
        while (i1 < len(combined_dataset_man[i])):
            if combined_dataset_man[i][i1] == []:
                del combined_dataset_man[i][i1]
            else:
                i1 = i1 + 1
        i = i + 1

i = 0
i1 = -1
i2 = -1
i3 = 0
for line in csv_reader2:
    if len(line) == 0:
        i = i + 1
    elif len(line) == 1:
        if i1 != i:
            i1 = i
            segmented_dataset_man.append([i1])
            i2 = i2 + 1
            segmented_dataset_man[i2].append([])
            i3 = 1
        else:
            segmented_dataset_man[i2].append([])
            i3 = i3 + 1
    elif len(line) == 3:
        #print(i,i1,i2)
        segmented_dataset_man[i2][i3].append([int(line[0]), int(line[1]), int(line[2])])

for line in csv_reader3:
    if len(line) > 0:
        fat_areas_mac.append(line)

"""print('len:', len(combined_dataset))
for i in combined_dataset[0]:
    print(i)

print()
print('len:', len(segmented_dataset))
for i in segmented_dataset[10]:
    print(i)"""

def take_second(elem):
    return elem[1]

def fats():
    global img_grid
    global img_grid_man
    
    #img_grid1 = []
    #for i in img_grid:
    #    img_grid1.append([])

    combined_fats_man = [] # used to record the combined datasets which are fats
    count_dataset = -1
    for line in combined_dataset_man:
        count_dataset = count_dataset + 1
        for i in line:
            #if len(i) > 0:
            x_i = int(i[0][0]) % x_total
            y_i = math.floor(int(i[0][0]) / x_total)
            x_i = x_i * s_size
            y_i = y_i * s_size
            i1 = 1
            while (i1 < len(i)):
                i2 = int(i[i1][1])
                while (i2 <= int(i[i1][2])):
                    img_grid_man[((y_i + int(i[i1][0])) * x_axis) + x_i + i2].append([count_dataset])
                    i2 = i2 + 1
                i1 = i1 + 1
        combined_fats_man.append([count_dataset, 0, 0])
    #print('combined_fats_manual:', len(combined_fats_man))

    segmented_fats_man = [] # used to record the combined datasets which are fats
    count_dataset = -1
    for line in segmented_dataset_man:
        count_dataset = count_dataset + 1
        x_i = line[0] % x_total
        y_i = math.floor(line[0] / x_total)
        x_i = x_i * s_size
        y_i = y_i * s_size

        segmented_fats_man.append([])
        for i in range(1,len(line)):
            i1 = 0
            while (i1 < len(line[i])):
                i2 = int(line[i][i1][1])
                while (i2 <= int(line[i][i1][2])):
                    img_grid_man[((y_i + int(line[i][i1][0])) * x_axis) + x_i + i2].append([count_dataset, i])
                    i2 = i2 + 1
                i1 = i1 + 1
            segmented_fats_man[count_dataset].append([count_dataset, i, 0, 0])
    #print('segmented_fats_manual:', len(segmented_fats_man))

    combined_fats_final_man = []
    i = 0
    for line in combined_fats_man:
        combined_fats_final_man.append(line[0])
        i = i + 1

    segmented_fats_final_man = []
    i1 = 0
    while (i1 < len(segmented_fats_man)):
        i2 = 0
        while (i2 < len(segmented_fats_man[i1])):
            segmented_fats_final_man.append(segmented_fats_man[i1][i2])
            i2 = i2 + 1
        i1 = i1 + 1

    combined_fats_area_man = []
    segmented_fats_area_man = []

    # calculate area of manually annotated
    i = 0
    while (i < len(combined_fats_final_man)):
        temp1 = 0
        for line in combined_dataset_man[combined_fats_final_man[i]]:
            i1 = 1
            while (i1 < len(line)):
                i2 = int(line[i1][1])
                while (i2 <= int(line[i1][2])):
                    temp1 = temp1 + 1
                    i2 = i2 + 1
                i1 = i1 + 1
        combined_fats_area_man.append(temp1)
        i = i + 1
    
    i = 0
    while (i < len(segmented_fats_final_man)):
        temp1 = 0
        i1 = 0
        while (i1 < len(segmented_dataset_man[segmented_fats_final_man[i][0]][segmented_fats_final_man[i][1]])):
            i2 = int(segmented_dataset_man[segmented_fats_final_man[i][0]][segmented_fats_final_man[i][1]][i1][1])
            while (i2 <= int(segmented_dataset_man[segmented_fats_final_man[i][0]][segmented_fats_final_man[i][1]][i1][2])):
                temp1 = temp1 + 1
                i2 = i2 + 1
            i1 = i1 + 1
        segmented_fats_area_man.append(temp1)
        i = i + 1

    """for i in range(len(combined_fats_final_man)):
        #print(combined_fats_final[i], combined_fats_area[i])
        print(i, combined_fats_area_man[i])
    print()
    for i in range(len(segmented_fats_final_man)):
        print(i, segmented_fats_area_man[i])"""
    total_manual_area = 0
    manual_annot_fat_seg = 0
    for i in range(len(combined_fats_final_man)):
        total_manual_area = total_manual_area + combined_fats_area_man[i]
        manual_annot_fat_seg = manual_annot_fat_seg + 1
    for i in range(len(segmented_fats_final_man)):
        total_manual_area = total_manual_area + segmented_fats_area_man[i]
        manual_annot_fat_seg = manual_annot_fat_seg + 1
    #print('manually annotated area:', total_manual_area, manual_annot_fat_seg)
    print('Manually annotated area: ', total_manual_area)  
    #print()
    total_machine_area = int(fat_areas_mac[-1][1])
    print('Machine annotated area: ', total_machine_area)
    
    print()
    total_valid_area = 0
    y_i = 0
    while (y_i < y_axis):
        x_i = 0
        while (x_i < x_axis):
            if imarray2[y_i][x_i][0] == r_val_man and imarray2[y_i][x_i][1] == g_val_man and imarray2[y_i][x_i][2] == b_val_man:
                #print('true')
                if imarray1[y_i][x_i][0] == r_val_mac and imarray1[y_i][x_i][1] == g_val_mac and imarray1[y_i][x_i][2] == b_val_mac:
                    imarray1[y_i][x_i][0] = r_val_int
                    imarray1[y_i][x_i][1] = g_val_int
                    imarray1[y_i][x_i][2] = b_val_int
                    total_valid_area = total_valid_area + 1
                else:
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