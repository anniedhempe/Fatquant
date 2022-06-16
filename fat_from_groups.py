from PIL import Image
import numpy as np
import math
import random
#import cv2 as cv
import skimage
import skimage.viewer
import csv

Image.MAX_IMAGE_PIXELS = None
original_image_name = input("Enter original image name with extension: ")
#ip_img = Image.open('shot5.tif')
ip_img = Image.open(original_image_name)
#ip_img = Image.open('E:/Annie Madam/Biology/Pancreas/liver_images/fatty/samples/' + str(original_image_name))
imarray = np.array(ip_img)
threshold_image_name = input("Enter thresholded image name with extension: ")
#ip_img = Image.open('human1_bi_m.png')
ip_img = Image.open(threshold_image_name)
#ip_img = Image.open('E:/Annie Madam/Biology/Pancreas/liver_images/fatty/thresholded_samples/' + str(threshold_image_name))
imarray1 = np.array(ip_img)
ip_img.close()
print(imarray.shape)

y_axis = imarray.shape[0] # 680 # size of each section
x_axis = imarray.shape[1]
total_pixels = x_axis * y_axis
s_size = 70 # size of each section (tile)
y_total = math.ceil(y_axis / s_size)
x_total = math.ceil(x_axis / s_size)
yx_total = y_total * x_total

output_image_name = input("Enter output image name (exclude exrtension): ")
image_o_exten = ''

i = len(original_image_name) - 1
while (original_image_name[i] != '.'):
    image_o_exten = image_o_exten + original_image_name[i]
    i = i - 1
image_o_exten = image_o_exten[::-1]

ip_img = []

img_grid = []
for i in range(total_pixels):
    img_grid.append([])

group_names = input("Enter 'y' for default white group names: ")
if group_names == 'y':
    combined_file = open('white_groups_combined.csv', 'r', newline='', encoding='utf16')
    csv_reader1 = csv.reader(combined_file)
    segmented_file = open('white_groups_segmented.csv', 'r', newline='', encoding='utf16')
    csv_reader2 = csv.reader(segmented_file)
else:
    combined_name = input("Enter white groups combined name (extension 'csv'): ")
    segmented_name = input("Enter white groups segmented name (extension 'csv'): ")
    combined_file = open(combined_name, 'r', newline='', encoding='utf16')
    csv_reader1 = csv.reader(combined_file)
    segmented_file = open(segmented_name, 'r', newline='', encoding='utf16')
    csv_reader2 = csv.reader(segmented_file)

combined_dataset = [[[]]]
segmented_dataset = []

fat_min_diameter = input("Enter minimum fat diameter: ")
output_image_name = output_image_name + '_' + fat_min_diameter
fat_min_diameter = int(fat_min_diameter)
fat_min_diameter = round(fat_min_diameter / math.sqrt(2))
print('min square side:', fat_min_diameter)
fat_max_diameter = input("Enter maximum fat diameter: ")
output_image_name = output_image_name + '_' + fat_max_diameter
fat_max_diameter = int(fat_max_diameter)
fat_max_diameter = round(fat_max_diameter / math.sqrt(2))
print('max square side:', fat_max_diameter)

i = 0
i1 = -1
for line in csv_reader1:
    if len(line) == 0:
        combined_dataset.append([])
        i = i + 1
        i1 = -1
    else:
        if len(line) == 3:
            combined_dataset[i][i1].append([int(line[0]), int(line[1]), int(line[2])])
        elif len(line) == 2:
            combined_dataset[i].append([])
            i1 = i1 + 1
            combined_dataset[i][i1].append([int(line[0]), int(line[1])])
i = 0 # remove null lists
while (i < len(combined_dataset)):
    if len(combined_dataset[i]) == 0:
        del combined_dataset[i]
    else:
        i1 = 0
        while (i1 < len(combined_dataset[i])):
            if combined_dataset[i][i1] == []:
                del combined_dataset[i][i1]
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
            segmented_dataset.append([i1])
            i2 = i2 + 1
            segmented_dataset[i2].append([])
            i3 = 1
        else:
            segmented_dataset[i2].append([])
            i3 = i3 + 1
    elif len(line) == 3:
        #print(i,i1,i2)
        segmented_dataset[i2][i3].append([int(line[0]), int(line[1]), int(line[2])])

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
    
    #img_grid1 = []
    #for i in img_grid:
    #    img_grid1.append([])

    combined_fats = [] # used to record the combined datasets which are fats
    count_dataset = -1
    for line in combined_dataset:
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
                    img_grid[((y_i + int(i[i1][0])) * x_axis) + x_i + i2].append([count_dataset])
                    i2 = i2 + 1
                i1 = i1 + 1
        combined_fats.append([count_dataset, 0, 0])
    print('combined_fats:', len(combined_fats))

    segmented_fats = [] # used to record the combined datasets which are fats
    count_dataset = -1
    for line in segmented_dataset:
        count_dataset = count_dataset + 1
        x_i = line[0] % x_total
        y_i = math.floor(line[0] / x_total)
        x_i = x_i * s_size
        y_i = y_i * s_size

        segmented_fats.append([])
        for i in range(1,len(line)):
            i1 = 0
            while (i1 < len(line[i])):
                i2 = int(line[i][i1][1])
                while (i2 <= int(line[i][i1][2])):
                    img_grid[((y_i + int(line[i][i1][0])) * x_axis) + x_i + i2].append([count_dataset, i])
                    i2 = i2 + 1
                i1 = i1 + 1
            segmented_fats[count_dataset].append([count_dataset, i, 0, 0])
    print('segmented_fats:', len(segmented_fats))

    border_thickness = [0, 0, 0, 0] # top, bottom, left, right
    i1 = 0 # top
    while (i1 < y_axis):
        i2 = 0
        while (i2 < x_axis):
            if imarray1[i1][i2][0] == 0 and imarray1[i1][i2][1] == 0 and imarray1[i1][i2][2] == 0:
                i2 = i2 + 1
            else:
                break
        if i2 != x_axis:
            border_thickness[0] = i1 - 1
            break
        i1 = i1 + 1
    i1 = y_axis - 1 # bottom
    while (i1 >= 0):
        i2 = 0
        while (i2 < x_axis):
            if imarray1[i1][i2][0] == 0 and imarray1[i1][i2][1] == 0 and imarray1[i1][i2][2] == 0:
                i2 = i2 + 1
            else:
                break
        if i2 != x_axis:
            border_thickness[1] = i1 + 1
            break
        i1 = i1 - 1
    i2 = 0 # left
    while (i2 < x_axis):
        i1 = 0
        while (i1 < y_axis):
            if imarray1[i1][i2][0] == 0 and imarray1[i1][i2][1] == 0 and imarray1[i1][i2][2] == 0:
                i1 = i1 + 1
            else:
                break
        if i1 != y_axis:
            border_thickness[2] = i2 - 1
            break
        i2 = i2 + 1
    i2 = x_axis - 1 # right
    while (i2 >= 0):
        i1 = 0
        while (i1 < y_axis):
            if imarray1[i1][i2][0] == 0 and imarray1[i1][i2][1] == 0 and imarray1[i1][i2][2] == 0:
                i1 = i1 + 1
            else:
                break
        if i1 != y_axis:
            border_thickness[3] = i2 + 1
            break
        i2 = i2 - 1
    print('border_thickness:', border_thickness)

    j_y_axis = border_thickness[0] + 1
    j_y_axis_r = border_thickness[0] + 1 + fat_min_diameter - 1 # fat_min_diameter - 1
    #while (j_y_axis_r < (border_thickness[1] - 1)):
    while (j_y_axis_r < (border_thickness[1] - 1)):
        #print(j_y_axis_r,border_thickness[1] - 1)
        j_x_axis = border_thickness[2] + 1
        j_x_axis_r = border_thickness[2] + 1 + fat_min_diameter - 1 # fat_min_diameter - 1

        #while (j_x_axis_r < border_thickness[3] - 1):
        while (j_x_axis_r < border_thickness[3] - 1):
            flag1 = 0
            temp1 = img_grid[(j_y_axis * x_axis) + j_x_axis]
            #temp1 = img_grid[(j_y_axis * (border_thickness[3] - border_thickness[2] - 1)) + j_x_axis]
            if len(temp1) > 0:
                if len(temp1[0]) == 1:
                    if combined_fats[temp1[0][0]][2] == fat_min_diameter:
                        j_x_axis = j_x_axis + 1
                        j_x_axis_r = j_x_axis_r + 1
                    else:
                        j1 = 0 # for Y
                        while (j1 < fat_min_diameter):
                            if flag1 == 1:
                                break
                            j2 = j_x_axis
                            while (j2 <= j_x_axis_r):
                                if img_grid[(j_y_axis * x_axis) + j2 + (j1 * x_axis)] == temp1:
                                    #if img_grid[(j_y_axis * (border_thickness[3] - border_thickness[2] - 1)) + j2 + (j1 * (border_thickness[3] - border_thickness[2] - 1))] == temp1:
                                    j2 = j2 + 1
                                else:
                                    flag1 = 1
                                    break
                            j1 = j1 + 1
                        if flag1 == 0:
                            if len(temp1) > 0:
                                if len(temp1[0]) == 1:
                                    combined_fats[temp1[0][0]][1] = 1
                                    combined_fats[temp1[0][0]][2] = fat_min_diameter
                                else:
                                    j = 0
                                    while (j < len(segmented_fats[temp1[0][0]])):
                                        if segmented_fats[temp1[0][0]][j][1] == temp1[0][1]:
                                            segmented_fats[temp1[0][0]][j][2] = 1
                                            segmented_fats[temp1[0][0]][j][3] = fat_min_diameter
                                            break
                                        j = j + 1

                        j_x_axis = j_x_axis + 1
                        j_x_axis_r = j_x_axis_r + 1
                        
                else:
                    j = 0
                    while (j < len(segmented_fats[temp1[0][0]])):
                        if segmented_fats[temp1[0][0]][j][1] == temp1[0][1] and segmented_fats[temp1[0][0]][j][3] == fat_min_diameter:
                            break
                        j = j + 1
                    if j == len(segmented_fats[temp1[0][0]]):
                        j1 = 0 # for Y
                        while (j1 < fat_min_diameter):
                            if flag1 == 1:
                                break
                            j2 = j_x_axis
                            while (j2 <= j_x_axis_r):
                                if img_grid[(j_y_axis * x_axis) + j2 + (j1 * x_axis)] == temp1:
                                    #if img_grid[(j_y_axis * (border_thickness[3] - border_thickness[2] - 1)) + j2 + (j1 * (border_thickness[3] - border_thickness[2] - 1))] == temp1:
                                    j2 = j2 + 1
                                else:
                                    flag1 = 1
                                    break
                            j1 = j1 + 1
                        if flag1 == 0:
                            if len(temp1) > 0:
                                if len(temp1[0]) == 1:
                                    combined_fats[temp1[0][0]][1] = 1
                                    combined_fats[temp1[0][0]][2] = fat_min_diameter
                                else:
                                    j = 0
                                    while (j < len(segmented_fats[temp1[0][0]])):
                                        if segmented_fats[temp1[0][0]][j][1] == temp1[0][1]:
                                            segmented_fats[temp1[0][0]][j][2] = 1
                                            segmented_fats[temp1[0][0]][j][3] = fat_min_diameter
                                            break
                                        j = j + 1

                    j_x_axis = j_x_axis + 1
                    j_x_axis_r = j_x_axis_r + 1
            
            else:
                j1 = 0 # for Y
                while (j1 < fat_min_diameter):
                    if flag1 == 1:
                        break
                    j2 = j_x_axis
                    while (j2 <= j_x_axis_r):
                        if img_grid[(j_y_axis * x_axis) + j2 + (j1 * x_axis)] == temp1:
                            #if img_grid[(j_y_axis * (border_thickness[3] - border_thickness[2] - 1)) + j2 + (j1 * (border_thickness[3] - border_thickness[2] - 1))] == temp1:
                            j2 = j2 + 1
                        else:
                            flag1 = 1
                            break
                    j1 = j1 + 1
                if flag1 == 0:
                    if len(temp1) > 0:
                        if len(temp1[0]) == 1:
                            combined_fats[temp1[0][0]][1] = 1
                            combined_fats[temp1[0][0]][2] = fat_min_diameter
                        else:
                            j = 0
                            while (j < len(segmented_fats[temp1[0][0]])):
                                if segmented_fats[temp1[0][0]][j][1] == temp1[0][1]:
                                    segmented_fats[temp1[0][0]][j][2] = 1
                                    segmented_fats[temp1[0][0]][j][3] = fat_min_diameter
                                    break
                                j = j + 1

                j_x_axis = j_x_axis + 1
                j_x_axis_r = j_x_axis_r + 1
        j_y_axis = j_y_axis + 1
        j_y_axis_r = j_y_axis_r + 1
    
    if fat_max_diameter > fat_min_diameter:
        j_y_axis = border_thickness[0] + 1
        j_y_axis_r = border_thickness[0] + 1 + fat_max_diameter - 1 # fat_max_diameter - 1
        #while (j_y_axis_r < y_axis - 1):
        #while (j_y_axis_r < (border_thickness[1] - 1)):
        while (j_y_axis_r < (border_thickness[1] - 1)):
            #print(j_y_axis_r,(border_thickness[1] - 1))
            j_x_axis = border_thickness[2] + 1
            j_x_axis_r = border_thickness[2] + 1 + fat_max_diameter - 1 # fat_max_diameter - 1

            #while (j_x_axis_r < x_axis - 1):
            #while (j_x_axis_r < (border_thickness[3] - 1)):
            while (j_x_axis_r < (border_thickness[3] - 1)):
                flag1 = 0
                temp1 = img_grid[(j_y_axis * x_axis) + j_x_axis]
                #temp1 = img_grid[(j_y_axis * (border_thickness[3] - border_thickness[2] - 1)) + j_x_axis]
                if len(temp1) > 0:
                    if len(temp1[0]) == 1:
                        if combined_fats[temp1[0][0]][2] == fat_max_diameter:
                            j_x_axis = j_x_axis + 1
                            j_x_axis_r = j_x_axis_r + 1
                        else:
                            j1 = 0 # for Y
                            while (j1 < fat_max_diameter):
                                if flag1 == 1:
                                    break
                                j2 = j_x_axis
                                while (j2 <= j_x_axis_r):
                                    if img_grid[(j_y_axis * x_axis) + j2 + (j1 * x_axis)] == temp1:
                                        #if img_grid[(j_y_axis * (border_thickness[3] - border_thickness[2] - 1)) + j2 + (j1 * (border_thickness[3] - border_thickness[2] - 1))] == temp1:
                                        j2 = j2 + 1
                                    else:
                                        flag1 = 1
                                        break
                                j1 = j1 + 1
                            if flag1 == 0:
                                if len(temp1) > 0:
                                    if len(temp1[0]) == 1:
                                        combined_fats[temp1[0][0]][2] = fat_max_diameter
                                    else:
                                        j = 0
                                        while (j < len(segmented_fats[temp1[0][0]])):
                                            if segmented_fats[temp1[0][0]][j][1] == temp1[0][1]:
                                                segmented_fats[temp1[0][0]][j][3] = fat_max_diameter
                                                break
                                            j = j + 1

                            j_x_axis = j_x_axis + 1
                            j_x_axis_r = j_x_axis_r + 1
                        
                    else:
                        j = 0
                        while (j < len(segmented_fats[temp1[0][0]])):
                            if segmented_fats[temp1[0][0]][j][1] == temp1[0][1] and segmented_fats[temp1[0][0]][j][3] == fat_max_diameter:
                                break
                            j = j + 1
                        if j == len(segmented_fats[temp1[0][0]]):
                            j1 = 0 # for Y
                            while (j1 < fat_max_diameter):
                                if flag1 == 1:
                                    break
                                j2 = j_x_axis
                                while (j2 <= j_x_axis_r):
                                    if img_grid[(j_y_axis * x_axis) + j2 + (j1 * x_axis)] == temp1:
                                        #if img_grid[(j_y_axis * (border_thickness[3] - border_thickness[2] - 1)) + j2 + (j1 * (border_thickness[3] - border_thickness[2] - 1))] == temp1:    
                                        j2 = j2 + 1
                                    else:
                                        flag1 = 1
                                        break
                                j1 = j1 + 1
                            if flag1 == 0:
                                if len(temp1) > 0:
                                    if len(temp1[0]) == 1:
                                        combined_fats[temp1[0][0]][2] = fat_max_diameter
                                    else:
                                        j = 0
                                        while (j < len(segmented_fats[temp1[0][0]])):
                                            if segmented_fats[temp1[0][0]][j][1] == temp1[0][1]:
                                                segmented_fats[temp1[0][0]][j][3] = fat_max_diameter
                                                break
                                            j = j + 1

                        j_x_axis = j_x_axis + 1
                        j_x_axis_r = j_x_axis_r + 1
            
                else:
                    j1 = 0 # for Y
                    while (j1 < fat_max_diameter):
                        if flag1 == 1:
                            break
                        j2 = j_x_axis
                        while (j2 <= j_x_axis_r):
                            if img_grid[(j_y_axis * x_axis) + j2 + (j1 * x_axis)] == temp1:
                                #if img_grid[(j_y_axis * (border_thickness[3] - border_thickness[2] - 1)) + j2 + (j1 * (border_thickness[3] - border_thickness[2] - 1))] == temp1:
                                j2 = j2 + 1
                            else:
                                flag1 = 1
                                break
                        j1 = j1 + 1
                    if flag1 == 0:
                        if len(temp1) > 0:
                            if len(temp1[0]) == 1:
                                combined_fats[temp1[0][0]][2] = fat_max_diameter
                            else:
                                j = 0
                                while (j < len(segmented_fats[temp1[0][0]])):
                                    if segmented_fats[temp1[0][0]][j][1] == temp1[0][1]:
                                        segmented_fats[temp1[0][0]][j][3] = fat_max_diameter
                                        break
                                    j = j + 1

                    j_x_axis = j_x_axis + 1
                    j_x_axis_r = j_x_axis_r + 1
            j_y_axis = j_y_axis + 1
            j_y_axis_r = j_y_axis_r + 1

    combined_dataset_boundary = []
    #combined_dataset_boundary1 = []
    i = 0 # remove groups of combined_dataset having edges in boundary
    while (i < len(combined_dataset)):
        i1 = 0
        flag1 = 0
        #flag2 = [0,0,0]
        if combined_fats[i][2] == fat_min_diameter:
            while (i1 < len(combined_dataset[i])):
                if combined_dataset[i][i1][0][0] == 0:
                    if combined_dataset[i][i1][1][0] == 0:
                        flag1 = 1
                        #flag2 = [1, combined_dataset[i][i1][0][0], combined_dataset[i][i1][1][0]]
                        break
                    else:
                        i2 = 1
                        while (i2 < len(combined_dataset[i][i1])):
                            if combined_dataset[i][i1][i2][1] == 0:
                                flag1 = 1
                                #flag2 = [1, combined_dataset[i][i1][0][0], combined_dataset[i][i1][i2][1]]
                                break
                            i2 = i2 + 1
                        if flag1 == 1:
                            break
                elif combined_dataset[i][i1][0][0] >= 1 and combined_dataset[i][i1][0][0] < x_total - 1:
                    if combined_dataset[i][i1][1][0] == 0:
                        flag1 = 1
                        #flag2 = [2, combined_dataset[i][i1][0][0], combined_dataset[i][i1][1][0]]
                        break
                elif combined_dataset[i][i1][0][0] == x_total - 1:
                    if combined_dataset[i][i1][1][0] == 0:
                        flag1 = 1
                        #flag2 = [3, combined_dataset[i][i1][0][0], combined_dataset[i][i1][1][0]]
                        break
                    else:
                        i2 = 1
                        while (i2 < len(combined_dataset[i][i1])):
                            if ((x_total - 1) * s_size) + combined_dataset[i][i1][i2][2] == x_axis - 1:
                                #if combined_dataset[i][i1][i2][2] == x_axis - 1: # 99
                                flag1 = 1
                                #flag2 = [3, combined_dataset[i][i1][0][0], combined_dataset[i][i1][i2][2]]
                                break
                            i2 = i2 + 1
                        if flag1 == 1:
                            break
                elif combined_dataset[i][i1][0][0] % x_total == 0:
                    i2 = 1
                    while (i2 < len(combined_dataset[i][i1])):
                        if combined_dataset[i][i1][i2][1] == 0:
                            flag1 = 1
                            #flag2 = [4, combined_dataset[i][i1][0][0], combined_dataset[i][i1][i2][1]]
                            break
                        i2 = i2 + 1
                    if flag1 == 1:
                        break
                elif (combined_dataset[i][i1][0][0] + 1) % x_total == 0:
                    i2 = 1
                    while (i2 < len(combined_dataset[i][i1])):
                        if ((x_total - 1) * s_size) + combined_dataset[i][i1][i2][2] == x_axis - 1:
                            #if combined_dataset[i][i1][i2][2] == x_axis - 1:
                            flag1 = 1
                            #flag2 = [5, combined_dataset[i][i1][0][0], combined_dataset[i][i1][i2][2]]
                            break
                        i2 = i2 + 1
                    if flag1 == 1:
                        break
                elif combined_dataset[i][i1][0][0] == (yx_total - x_total):
                    if ((y_total - 1) * s_size) + combined_dataset[i][i1][len(combined_dataset[i][i1]) - 1][0] == y_axis - 1:
                        #if combined_dataset[i][i1][len(combined_dataset[i][i1]) - 1][0] == 99:
                        flag1 = 1
                        #flag2 = [6, combined_dataset[i][i1][0][0], combined_dataset[i][i1][len(combined_dataset[i][i1]) - 1][0]]
                        break
                    else:
                        i2 = 1
                        while (i2 < len(combined_dataset[i][i1])):
                            if combined_dataset[i][i1][i2][1] == 0:
                                flag1 = 1
                                #flag2 = [6, combined_dataset[i][i1][0][0], combined_dataset[i][i1][i2][1]]
                                break
                            i2 = i2 + 1
                        if flag1 == 1:
                            break
                elif combined_dataset[i][i1][0][0] >= (yx_total - x_total + 1) and combined_dataset[i][i1][0][0] < yx_total - 1:
                    if ((y_total - 1) * s_size) + combined_dataset[i][i1][len(combined_dataset[i][i1]) - 1][0] == y_axis - 1:
                        #if combined_dataset[i][i1][len(combined_dataset[i][i1]) - 1][0] == 99:
                        flag1 = 1
                        #flag2 = [7, combined_dataset[i][i1][0][0], combined_dataset[i][i1][len(combined_dataset[i][i1]) - 1][0]]
                        break
                elif combined_dataset[i][i1][0][0] == yx_total - 1:
                    if ((y_total - 1) * s_size) + combined_dataset[i][i1][len(combined_dataset[i][i1]) - 1][0] == y_axis - 1:    
                        #if combined_dataset[i][i1][len(combined_dataset[i][i1]) - 1][0] == 99:
                        flag1 = 1
                        #flag2 = [8, combined_dataset[i][i1][0][0], combined_dataset[i][i1][len(combined_dataset[i][i1]) - 1][0]]
                        break
                    else:
                        i2 = 1
                        while (i2 < len(combined_dataset[i][i1])):
                            if ((x_total - 1) * s_size) + combined_dataset[i][i1][i2][2] == x_axis - 1:
                                #if combined_dataset[i][i1][i2][2] == 99:
                                flag1 = 1
                                #flag2 = [8, combined_dataset[i][i1][0][0], combined_dataset[i][i1][i2][2]]
                                break
                            i2 = i2 + 1
                        if flag1 == 1:
                            break
            
                i1 = i1 + 1
        if flag1 == 1:
            #del combined_dataset[i]
            #del combined_fats[i]
            combined_dataset_boundary.append(i)
            #combined_dataset_boundary1.append([flag2, i])
            i = i + 1
        else:
            i = i + 1
    print('combined_boundary:', len(combined_dataset_boundary))
    #print('combined_boundary1:')
    #for i in combined_dataset_boundary1:
    #    print(i)
    """i = 0 # rename indices of combined_fats
    while (i < len(combined_fats)):
        combined_fats[i][0] = i
        i = i + 1"""

    segmented_dataset_boundary = []
    for i in range(len(segmented_fats)):
        segmented_dataset_boundary.append([])
    
    i = 0 # remove groups of segmented_dataset having edges in boundary
    j = 0
    while (j < len(segmented_dataset)):
        if segmented_dataset[j][0] == 0:
            i = 1
            while (i < len(segmented_dataset[j])):
                i1 = 0
                flag1 = 0
                if segmented_fats[j][i - 1][3] == fat_min_diameter:
                    #print('found: ', j, i, i - 1, segmented_fats[j][i - 1])
                    while (i1 < len(segmented_dataset[j][i])):
                        if segmented_dataset[j][i][i1][0] == 0:
                            #if segmented_dataset[j][i][i1][1] == 0:
                            flag1 = 1
                            break
                        else:
                            i2 = i1
                            while (i2 < len(segmented_dataset[j][i])):
                                if segmented_dataset[j][i][i2][1] == 0:
                                    flag1 = 1
                                    break
                                i2 = i2 + 1
                            i1 = i2
                            if flag1 == 1:
                                break
                if flag1 == 1:
                    segmented_dataset_boundary[j].append(i - 1)
                    #print('found: ', j, i, i - 1, segmented_fats[j][i - 1])
                    #print('appended: ', i)
                    i = i + 1
                else:
                    i = i + 1

        if segmented_dataset[j][0] >= 1 and segmented_dataset[j][0] < x_total - 1:
            i = 1
            while (i < len(segmented_dataset[j])):
                i1 = 0
                flag1 = 0
                if segmented_fats[j][i - 1][3] == fat_min_diameter:
                    if segmented_dataset[j][i][0][0] == 0:
                        flag1 = 1
                if flag1 == 1:
                    segmented_dataset_boundary[j].append(i - 1)
                    i = i + 1
                else:
                    i = i + 1

        if segmented_dataset[j][0] == x_total - 1:
            i = 1
            while (i < len(segmented_dataset[j])):
                i1 = 0
                flag1 = 0
                if segmented_fats[j][i - 1][3] == fat_min_diameter:
                    while (i1 < len(segmented_dataset[j][i])):
                        if segmented_dataset[j][i][i1][0] == 0:
                            #if segmented_dataset[j][i][i1][1] == 0:
                            flag1 = 1
                            break
                        else:
                            i2 = i1
                            while (i2 < len(segmented_dataset[j][i])):
                                if ((x_total - 1) * s_size) + segmented_dataset[j][i][i2][2] == x_axis - 1:
                                    flag1 = 1
                                    break
                                i2 = i2 + 1
                            i1 = i2
                            if flag1 == 1:
                                break
                if flag1 == 1:
                    segmented_dataset_boundary[j].append(i - 1)
                    i = i + 1
                else:
                    i = i + 1
        
        if segmented_dataset[j][0] % x_total == 0:
            i = 1
            while (i < len(segmented_dataset[j])):
                i1 = 0
                flag1 = 0
                if segmented_fats[j][i - 1][3] == fat_min_diameter:
                    while (i1 < len(segmented_dataset[j][i])):
                        if segmented_dataset[j][i][i1][1] == 0:
                            flag1 = 1
                            break
                        i1 = i1 + 1
                if flag1 == 1:
                    segmented_dataset_boundary[j].append(i - 1)
                    i = i + 1
                else:
                    i = i + 1
        
        if (segmented_dataset[j][0] + 1) % x_total == 0:
            i = 1
            while (i < len(segmented_dataset[j])):
                i1 = 0
                flag1 = 0
                if segmented_fats[j][i - 1][3] == fat_min_diameter:
                    while (i1 < len(segmented_dataset[j][i])):                        
                        if ((x_total - 1) * s_size) + segmented_dataset[j][i][i1][2] == x_axis - 1:
                            flag1 = 1
                            break
                        i1 = i1 + 1
                if flag1 == 1:
                    segmented_dataset_boundary[j].append(i - 1)
                    i = i + 1
                else:
                    i = i + 1

        if segmented_dataset[j][0] == (yx_total - x_total):
            i = 1
            while (i < len(segmented_dataset[j])):
                i1 = 0
                flag1 = 0
                if segmented_fats[j][i - 1][3] == fat_min_diameter:
                    #print('found: ', j, i, i - 1, segmented_fats[j][i - 1])
                    if ((y_total - 1) * s_size) + segmented_dataset[j][i][len(segmented_dataset[j][i]) - 1][0] == y_axis - 1:
                        flag1 = 1
                    else:
                        while (i1 < len(segmented_dataset[j][i])):
                            if segmented_dataset[j][i][i1][1] == 0:
                                flag1 = 1
                                break
                            i1 = i1 + 1
                if flag1 == 1:
                    segmented_dataset_boundary[j].append(i - 1)
                    #print('found: ', j, i, i - 1, segmented_fats[j][i - 1])
                    #print('appended: ', i)
                    i = i + 1
                else:
                    i = i + 1

        if segmented_dataset[j][0] >= (yx_total - x_total + 1) and segmented_dataset[j][0] < yx_total - 1:
            i = 1
            while (i < len(segmented_dataset[j])):
                i1 = 0
                flag1 = 0
                if segmented_fats[j][i - 1][3] == fat_min_diameter:
                    #print('found: ', j, i, i - 1, segmented_fats[j][i - 1])
                    if ((y_total - 1) * s_size) + segmented_dataset[j][i][len(segmented_dataset[j][i]) - 1][0] == y_axis - 1:
                        flag1 = 1
                if flag1 == 1:
                    segmented_dataset_boundary[j].append(i - 1)
                    #print('found: ', j, i, i - 1, segmented_fats[j][i - 1])
                    #print('appended: ', i)
                    i = i + 1
                else:
                    i = i + 1
        
        if segmented_dataset[j][0] == yx_total - 1:
            i = 1
            while (i < len(segmented_dataset[j])):
                i1 = 0
                flag1 = 0
                if segmented_fats[j][i - 1][3] == fat_min_diameter:
                    #print('found: ', j, i, i - 1, segmented_fats[j][i - 1])
                    if ((y_total - 1) * s_size) + segmented_dataset[j][i][len(segmented_dataset[j][i]) - 1][0] == y_axis - 1:
                        flag1 = 1
                    else:
                        while (i1 < len(segmented_dataset[j][i])):
                            if ((x_total - 1) * s_size) + segmented_dataset[j][i][i1][2] == x_axis - 1:
                                flag1 = 1
                                break
                            i1 = i1 + 1
                if flag1 == 1:
                    segmented_dataset_boundary[j].append(i - 1)
                    #print('found: ', j, i, i - 1, segmented_fats[j][i - 1])
                    #print('appended: ', i)
                    i = i + 1
                else:
                    i = i + 1
        j = j + 1

    temp1 = 0
    i = 0
    for j in segmented_dataset_boundary:
        temp1 = temp1 + len(j)
    print('segmented_boundary:', temp1)
    
    print()
    combined_fats_final = []
    i = 0
    for line in combined_fats:
        if combined_dataset_boundary.__contains__(i) == False:
            if line[1] == 1 and (line[2] < fat_max_diameter):
                combined_fats_final.append(line[0])
        i = i + 1
    print('valid combined:', len(combined_fats_final))

    segmented_fats_final = []
    i1 = 0
    while (i1 < len(segmented_fats)):
        i2 = 0
        while (i2 < len(segmented_fats[i1])):
            if segmented_dataset_boundary[i1].__contains__(i2) == False:
                if segmented_fats[i1][i2][2] == 1 and (segmented_fats[i1][i2][3] < fat_max_diameter):
                    segmented_fats_final.append(segmented_fats[i1][i2])
            """else:
                print('seg bd: ', i1, i2)"""
            i2 = i2 + 1
        i1 = i1 + 1
    print('valid segmented:', len(segmented_fats_final))

    i = 0
    while (i < total_pixels):
        if img_grid[i] != []:
            if len(img_grid[i][0]) == 1:
                if combined_fats_final.__contains__(img_grid[i][0][0]) == True:
                    x_i = i % x_axis
                    y_i = math.floor(i / x_axis)
                    imarray[y_i][x_i][0] = 0
                    imarray[y_i][x_i][1] = 255
                    imarray[y_i][x_i][2] = 255
            else:
                #print('output:', segmented_fats_final, img_grid[i][0])
                j = 0
                while (j < len(segmented_fats_final)):
                    if segmented_fats_final[j][0] == img_grid[i][0][0] and segmented_fats_final[j][1] == img_grid[i][0][1]:
                        x_i = i % x_axis
                        y_i = math.floor(i / x_axis)
                        imarray[y_i][x_i][0] = 0
                        imarray[y_i][x_i][1] = 255
                        imarray[y_i][x_i][2] = 255
                        break
                    j = j + 1
        i = i + 1

    combined_fats_area = []
    segmented_fats_area = []
    
    i = 0
    while (i < len(combined_fats_final)):
        temp1 = 0
        for line in combined_dataset[combined_fats_final[i]]:
            i1 = 1
            while (i1 < len(line)):
                i2 = int(line[i1][1])
                while (i2 <= int(line[i1][2])):
                    temp1 = temp1 + 1
                    i2 = i2 + 1
                i1 = i1 + 1
        combined_fats_area.append(temp1)
        i = i + 1
    
    i = 0
    while (i < len(segmented_fats_final)):
        temp1 = 0
        i1 = 0
        while (i1 < len(segmented_dataset[segmented_fats_final[i][0]][segmented_fats_final[i][1]])):
            i2 = int(segmented_dataset[segmented_fats_final[i][0]][segmented_fats_final[i][1]][i1][1])
            while (i2 <= int(segmented_dataset[segmented_fats_final[i][0]][segmented_fats_final[i][1]][i1][2])):
                temp1 = temp1 + 1
                i2 = i2 + 1
            i1 = i1 + 1
        segmented_fats_area.append(temp1)
        i = i + 1

    """for i in range(len(combined_fats_final)):
        #print(combined_fats_final[i], combined_fats_area[i])
        print(i, combined_fats_area[i])
    print()
    for i in range(len(segmented_fats_final)):
        print(i, segmented_fats_area[i])"""
    
    fat_areas = []
    fat_areas.append(['Sl. no.', 'Area (in pixels)'])
    total_fats = 0
    total_area = 0
    for i in range(len(combined_fats_final)):
        total_fats = total_fats + 1
        total_area = total_area + combined_fats_area[i]
        fat_areas.append([total_fats, combined_fats_area[i]])
    for i in range(len(segmented_fats_final)):
        total_fats = total_fats + 1
        total_area = total_area + segmented_fats_area[i]
        fat_areas.append([total_fats, segmented_fats_area[i]])
    fat_areas.append([])
    fat_areas.append(['total area', total_area])
    
    fat_areas_file = open(output_image_name + '.' + 'csv', 'w', newline='', encoding='utf16')
    #fat_areas_file = open('E:/Annie Madam/Biology/Pancreas/liver_images/fatty/areas_in_samples/' + output_image_name + '.' + 'csv', 'w', newline='', encoding='utf16')
    csv_write1 = csv.writer(fat_areas_file, delimiter = ',')
    # store area values
    for i in fat_areas:
        csv_write1.writerow(i)
    
    viewer = skimage.viewer.ImageViewer(imarray)
    viewer.show()
    data = Image.fromarray(imarray)
    #data.save('E:/Annie Madam/Biology/First Paper/10b.tif')
    data.save(output_image_name + '.' + image_o_exten)
    #data.save('E:/Annie Madam/Biology/Pancreas/liver_images/fatty/outputs/' + output_image_name + '.' + image_o_exten)

fats()