from PIL import Image
import numpy as np
#import matplotlib
#import matplotlib.pyplot as plt
import math
import random
#import pandas as pd
import cv2 as cv
import skimage
import skimage.viewer
import csv

image1 = input('Enter thresholded image name with extension: ')
#path_in = ('shot7_bi.tif')
path_in = (str(image1))
img=cv.imread(path_in)

imarray = np.array(img)
print(imarray.shape, imarray.size, len(imarray))
y_axis = imarray.shape[0] # 680 # size of each section
x_axis = imarray.shape[1]

s_size = 70 # size of each section

section_items = []
segmented_areas = []

def combine_segments(section_n):
    # combine segments xxx  ooo
    #                  xxxxxxxx
    global segmented_areas 
    i1 = 0
    while (i1 < len(segmented_areas[section_n])):
        i2 = i1 + 1
        while (i2 < len(segmented_areas[section_n])):
            flag3 = 0
            j2 = 2
            while (j2 < len(segmented_areas[section_n][i2])):
                j1 = 2
                while (j1 < len(segmented_areas[section_n][i1])):
                    if abs(segmented_areas[section_n][i2][j2][0] - segmented_areas[section_n][i1][j1][0]) == 1:
                        if segmented_areas[section_n][i1][j1][1] <= segmented_areas[section_n][i2][j2][1] and segmented_areas[section_n][i1][j1][2] >= segmented_areas[section_n][i2][j2][1]:
                            flag3 = 1
                        elif segmented_areas[section_n][i2][j2][1] <= segmented_areas[section_n][i1][j1][1] and segmented_areas[section_n][i2][j2][2] >= segmented_areas[section_n][i1][j1][1]:
                            flag3 = 1
                    elif segmented_areas[section_n][i1][j1][0] > segmented_areas[section_n][i2][j2][0] + 1:
                        break
                    j1 = j1 + 1
                j2 = j2 + 1

            if flag3 == 1:
                j2 = 2
                while (j2 < len(segmented_areas[section_n][i2])):
                    j1 = 2
                    flag1 = 0
                    while (flag1 < 1):
                        if (j1 < len(segmented_areas[section_n][i1])):
                            if (j1 < len(segmented_areas[section_n][i1]) - 1):
                                if (segmented_areas[section_n][i1][j1][0] == segmented_areas[section_n][i2][j2][0]) and (segmented_areas[section_n][i1][j1 + 1][0] > segmented_areas[section_n][i2][j2][0]):
                                    segmented_areas[section_n][i1].insert(j1 + 1, segmented_areas[section_n][i2][j2])
                                    flag1 = 1
                            else:
                                segmented_areas[section_n][i1].append(segmented_areas[section_n][i2][j2])
                                flag1 = 1
                            j1 = j1 + 1
                        else:
                            flag1 = 1
                    j2 = j2 + 1
                if segmented_areas[section_n][i1][1][1] < segmented_areas[section_n][i2][1][1]:
                    segmented_areas[section_n][i1][1][1] = segmented_areas[section_n][i2][1][1]
                del segmented_areas[section_n][i2]
            else:
                i2 = i2 + 1
        i1 = i1 + 1

def white_segments(y_axis, x_axis, s_size):
    global section_items
    global segmented_areas
    
    y_total = math.ceil(y_axis / s_size)
    x_total = math.ceil(x_axis / s_size)

    print(y_total, x_total, y_total * x_total)
    
    section_items = []
    for section_n in range(y_total * x_total):
        section_items.append([])
        for i in range(s_size):
            section_items[section_n].append([])
    
    
    flag_0 = 0 # 1 when all sections are covered
    #while (flag_0 == 0):
    j1 = 0
    j2 = 0
    i1 = 0
    while (i1 < y_total):
        j = 0
        while (j1 < (i1 * s_size) + s_size):
            if j1 < y_axis:
                j2 = 0
                i2 = 0
                while (i2 < x_total):
                    while (j2 < (i2 * s_size) + s_size):
                        if j2 < x_axis:
                            section_items[(i1 * x_total) + i2][j].append(imarray[j1][j2])
                            #section_items[(i1 * x_total) + i2][j].insert(0,imarray[j1][j2])
                            j2 = j2 + 1
                        else:
                            break
                    i2 = i2 + 1
                j1 = j1 + 1
                j = j + 1
            else:
                break
        i1 = i1 + 1
    
    # segment white areas
    segmented_areas = [] # [[s_nos],[Yt,Yb,[Y,Xl,Xr]]]
    y_pseudo_section = y_axis - ((y_total - 1) * s_size)
    x_pseudo_section = x_axis - ((x_total - 1) * s_size)

    for section_n in range(len(section_items)):
        segmented_areas.append([])
        temp_areas = [] # segemented area in each row
        if math.floor(section_n / x_total) < (y_total - 1):
            i1 = 0
            while (i1 < s_size):
                if (section_n % x_total) < (x_total - 1):    
                    i2 = 0
                    while (i2 < s_size):
                        if section_items[section_n][i1][i2][0] == 255:
                            if len(temp_areas) == 0:
                                temp_areas.append([[i1,i2,i2]])
                            else:
                                j1 = 0
                                while (j1 < len(temp_areas)):
                                    if i2 + (s_size * 0) == temp_areas[j1][len(temp_areas[j1]) - 1][2] + 1:
                                        temp_areas[j1][len(temp_areas[j1]) - 1][2] = temp_areas[j1][len(temp_areas[j1]) - 1][2] + 1
                                        break
                                    j1 = j1 + 1
                                if j1 == len(temp_areas):
                                    temp_areas.append([[i1,i2,i2]])
                        i2 = i2 + 1
                else:
                    i2 = 0
                    while (i2 < x_pseudo_section):
                        if section_items[section_n][i1][i2][0] == 255:
                            if len(temp_areas) == 0:
                                temp_areas.append([[i1,i2,i2]])
                            else:
                                j1 = 0
                                while (j1 < len(temp_areas)):
                                    if i2 + (s_size * 0) == temp_areas[j1][len(temp_areas[j1]) - 1][2] + 1:
                                        temp_areas[j1][len(temp_areas[j1]) - 1][2] = temp_areas[j1][len(temp_areas[j1]) - 1][2] + 1
                                        break
                                    j1 = j1 + 1
                                if j1 == len(temp_areas):
                                    temp_areas.append([[i1,i2,i2]])
                        i2 = i2 + 1
                if len(temp_areas) > 0:
                    i = 0
                    while (i < len(temp_areas)):
                        segmented_areas[section_n].append([[section_n],[i1,i1]])
                        i2 = 0
                        while(i2 < len(temp_areas[i])):
                            segmented_areas[section_n][len(segmented_areas[section_n]) - 1].append(temp_areas[i][i2])
                            i2 = i2 + 1
                        #segmented_areas.append(temp_areas[i])
                        temp_areas[i].insert(0, len(segmented_areas[section_n]) - 1)
                        i = i + 1
                    break
                i1 = i1 + 1
        else:
            i1 = 0
            while (i1 < y_pseudo_section):
                if (section_n % x_total) < (x_total - 1):    
                    i2 = 0
                    while (i2 < s_size):
                        if section_items[section_n][i1][i2][0] == 255:
                            if len(temp_areas) == 0:
                                temp_areas.append([[i1,i2,i2]])
                            else:
                                j1 = 0
                                while (j1 < len(temp_areas)):
                                    if i2 + (s_size * 0) == temp_areas[j1][len(temp_areas[j1]) - 1][2] + 1:
                                        temp_areas[j1][len(temp_areas[j1]) - 1][2] = temp_areas[j1][len(temp_areas[j1]) - 1][2] + 1
                                        break
                                    j1 = j1 + 1
                                if j1 == len(temp_areas):
                                    temp_areas.append([[i1,i2,i2]])
                        i2 = i2 + 1
                else:
                    i2 = 0
                    while (i2 < x_pseudo_section):
                        if section_items[section_n][i1][i2][0] == 255:
                            if len(temp_areas) == 0:
                                temp_areas.append([[i1,i2,i2]])
                            else:
                                j1 = 0
                                while (j1 < len(temp_areas)):
                                    if i2 + (s_size * 0) == temp_areas[j1][len(temp_areas[j1]) - 1][2] + 1:
                                        temp_areas[j1][len(temp_areas[j1]) - 1][2] = temp_areas[j1][len(temp_areas[j1]) - 1][2] + 1
                                        break
                                    j1 = j1 + 1
                                if j1 == len(temp_areas):
                                    temp_areas.append([[i1,i2,i2]])
                        i2 = i2 + 1
                if len(temp_areas) > 0:
                    i = 0
                    while (i < len(temp_areas)):
                        segmented_areas[section_n].append([[section_n],[i1,i1]])
                        i2 = 0
                        while(i2 < len(temp_areas[i])):
                            segmented_areas[section_n][len(segmented_areas[section_n]) - 1].append(temp_areas[i][i2])
                            i2 = i2 + 1
                        #segmented_areas.append(temp_areas[i])
                        temp_areas[i].insert(0, len(segmented_areas[section_n]) - 1)
                        i = i + 1
                    break
                i1 = i1 + 1
        
        temp_areas2 = []
        if math.floor(section_n / x_total) < (y_total - 1):
            i1 = i1 + 1
            while (i1 < s_size):
                if (section_n % x_total) < (x_total - 1):
                    i2 = 0
                    temp_areas2 = []
                    while (i2 < s_size):
                        if section_items[section_n][i1][i2][0] == 255:
                            if len(temp_areas2) == 0:
                                temp_areas2.append([[i1,i2,i2]])
                            else:
                                j1 = 0
                                while (j1 < len(temp_areas2)):
                                    if i2 + (s_size * 0) == temp_areas2[j1][len(temp_areas2[j1]) - 1][2] + 1:
                                        temp_areas2[j1][len(temp_areas2[j1]) - 1][2] = temp_areas2[j1][len(temp_areas2[j1]) - 1][2] + 1
                                        break
                                    j1 = j1 + 1
                                if j1 == len(temp_areas2):
                                    temp_areas2.append([[i1,i2,i2]])
                        i2 = i2 + 1
                else:
                    i2 = 0
                    temp_areas2 = []
                    while (i2 < x_pseudo_section):
                        if section_items[section_n][i1][i2][0] == 255:
                            if len(temp_areas2) == 0:
                                temp_areas2.append([[i1,i2,i2]])
                            else:
                                j1 = 0
                                while (j1 < len(temp_areas2)):
                                    if i2 + (s_size * 0) == temp_areas2[j1][len(temp_areas2[j1]) - 1][2] + 1:
                                        temp_areas2[j1][len(temp_areas2[j1]) - 1][2] = temp_areas2[j1][len(temp_areas2[j1]) - 1][2] + 1
                                        break
                                    j1 = j1 + 1
                                if j1 == len(temp_areas2):
                                    temp_areas2.append([[i1,i2,i2]])
                        i2 = i2 + 1
    
                j1 = 0
                # find logic for xxxxx  or  x  xx  or  xxxxx  or   xxx
                #                x  xx      xxxxx       xxx       xxxxx
                new_areas = []
                while (j1 < len(temp_areas2)):
                    j2 = 0
                    while (j2 < len(temp_areas)):
                        if (temp_areas[j2][1][1] >= temp_areas2[j1][0][1] and temp_areas[j2][1][1] <= temp_areas2[j1][0][2]) or \
                           (temp_areas[j2][1][2] <= temp_areas2[j1][0][2] and temp_areas[j2][1][2] >= temp_areas2[j1][0][1]) or \
                           (temp_areas2[j1][0][1] <= temp_areas[j2][1][1] and temp_areas2[j1][0][2] >= temp_areas[j2][1][2]) or \
                           (temp_areas[j2][1][1] <= temp_areas2[j1][0][1] and temp_areas[j2][1][2] >= temp_areas2[j1][0][2]):
                            segmented_areas[section_n][temp_areas[j2][0]].append(temp_areas2[j1][0])
                            if segmented_areas[section_n][temp_areas[j2][0]][1][1] < temp_areas2[j1][0][0]: # update Yb
                                segmented_areas[section_n][temp_areas[j2][0]][1][1] = temp_areas2[j1][0][0]
                            if isinstance(temp_areas2[j1][0], list):
                                temp_areas2[j1].insert(0, temp_areas[j2][0])
                            break
                        j2 = j2 + 1
                    if j2 == len(temp_areas):
                        new_areas.append(j1)
                    j1 = j1 + 1
    
                # append new areas to segmented_areas
                i = 0
                while (i < len(new_areas)):
                    segmented_areas[section_n].append([[section_n],[i1,i1]])
                    i2 = 0
                    while(i2 < len(temp_areas2[new_areas[i]])):
                        segmented_areas[section_n][len(segmented_areas[section_n]) - 1].append(temp_areas2[new_areas[i]][i2])
                        i2 = i2 + 1
                    #segmented_areas.append(temp_areas[i])
                    temp_areas2[new_areas[i]].insert(0, len(segmented_areas[section_n]) - 1)
                    i = i + 1
    
                temp_areas = []
                for i in temp_areas2:
                    temp_areas.append(i)
    
                i1 = i1 + 1
        else:
            i1 = i1 + 1
            while (i1 < y_pseudo_section):
                if (section_n % x_total) < (x_total - 1):
                    i2 = 0
                    temp_areas2 = []
                    while (i2 < s_size):
                        if section_items[section_n][i1][i2][0] == 255:
                            if len(temp_areas2) == 0:
                                temp_areas2.append([[i1,i2,i2]])
                            else:
                                j1 = 0
                                while (j1 < len(temp_areas2)):
                                    if i2 + (s_size * 0) == temp_areas2[j1][len(temp_areas2[j1]) - 1][2] + 1:
                                        temp_areas2[j1][len(temp_areas2[j1]) - 1][2] = temp_areas2[j1][len(temp_areas2[j1]) - 1][2] + 1
                                        break
                                    j1 = j1 + 1
                                if j1 == len(temp_areas2):
                                    temp_areas2.append([[i1,i2,i2]])
                        i2 = i2 + 1
                else:
                    i2 = 0
                    temp_areas2 = []
                    while (i2 < x_pseudo_section):
                        if section_items[section_n][i1][i2][0] == 255:
                            if len(temp_areas2) == 0:
                                temp_areas2.append([[i1,i2,i2]])
                            else:
                                j1 = 0
                                while (j1 < len(temp_areas2)):
                                    if i2 + (s_size * 0) == temp_areas2[j1][len(temp_areas2[j1]) - 1][2] + 1:
                                        temp_areas2[j1][len(temp_areas2[j1]) - 1][2] = temp_areas2[j1][len(temp_areas2[j1]) - 1][2] + 1
                                        break
                                    j1 = j1 + 1
                                if j1 == len(temp_areas2):
                                    temp_areas2.append([[i1,i2,i2]])
                        i2 = i2 + 1
    
                j1 = 0
                # find logic for xxxxx  or  x  xx  or  xxxxx  or   xxx
                #                x  xx      xxxxx       xxx       xxxxx
                new_areas = []
                while (j1 < len(temp_areas2)):
                    j2 = 0
                    while (j2 < len(temp_areas)):
                        if (temp_areas[j2][1][1] >= temp_areas2[j1][0][1] and temp_areas[j2][1][1] <= temp_areas2[j1][0][2]) or \
                           (temp_areas[j2][1][2] <= temp_areas2[j1][0][2] and temp_areas[j2][1][2] >= temp_areas2[j1][0][1]) or \
                           (temp_areas2[j1][0][1] <= temp_areas[j2][1][1] and temp_areas2[j1][0][2] >= temp_areas[j2][1][2]) or \
                           (temp_areas[j2][1][1] <= temp_areas2[j1][0][1] and temp_areas[j2][1][2] >= temp_areas2[j1][0][2]):
                            segmented_areas[section_n][temp_areas[j2][0]].append(temp_areas2[j1][0])
                            if segmented_areas[section_n][temp_areas[j2][0]][1][1] < temp_areas2[j1][0][0]: # update Yb
                                segmented_areas[section_n][temp_areas[j2][0]][1][1] = temp_areas2[j1][0][0]
                            if isinstance(temp_areas2[j1][0], list):
                                temp_areas2[j1].insert(0, temp_areas[j2][0])
                            break
                        j2 = j2 + 1
                    if j2 == len(temp_areas):
                        new_areas.append(j1)
                    j1 = j1 + 1
    
                # append new areas to segmented_areas
                i = 0
                while (i < len(new_areas)):
                    segmented_areas[section_n].append([[section_n],[i1,i1]])
                    i2 = 0
                    while(i2 < len(temp_areas2[new_areas[i]])):
                        segmented_areas[section_n][len(segmented_areas[section_n]) - 1].append(temp_areas2[new_areas[i]][i2])
                        i2 = i2 + 1
                    #segmented_areas.append(temp_areas[i])
                    temp_areas2[new_areas[i]].insert(0, len(segmented_areas[section_n]) - 1)
                    i = i + 1
    
                temp_areas = []
                for i in temp_areas2:
                    temp_areas.append(i)
    
                i1 = i1 + 1

        temp1 = 0
        flag1 = 0
        while (flag1 == 0):
            combine_segments(section_n)
            #print('len:', len(segmented_areas))
            if temp1 != len(segmented_areas[section_n]):
                temp1 = len(segmented_areas[section_n])
            else:
                flag1 = 1

    # sections in boundary of segments
    section_boundary = []
    y_pseudo_section = y_axis - ((y_total - 1) * s_size)
    x_pseudo_section = x_axis - ((x_total - 1) * s_size)
    for section_n in range(len(segmented_areas)):
        section_boundary.append([section_n])
        if len(segmented_areas[section_n]) > 0:
            if (section_n + 1) % x_total == 0:
                x_length = x_pseudo_section
            else:
                x_length = s_size - 1
            if int(section_n / x_total) == y_total - 1:
                y_length = y_pseudo_section
            else:
                y_length = s_size - 1
             
            i = 0 # top boundary -> 0
            while (i < len(segmented_areas[section_n])):
                flag1 = 0 # 1 if any section is present in boundary
                i0 = 2
                while (i0 < len(segmented_areas[section_n][i])):
                    if segmented_areas[section_n][i][i0][0] > 0:
                        break
                    else:
                        section_boundary[section_n].append([0,[i, segmented_areas[section_n][i][i0][1], segmented_areas[section_n][i][i0][2]]]) # [i, left, right]
                        flag1 = 1
                        i0 = i0 + 1
                        break
                
                if flag1 == 1:
                    while (i0 < len(segmented_areas[section_n][i])):
                        if segmented_areas[section_n][i][i0][0] > 0:
                            break
                        else:
                            section_boundary[section_n][len(section_boundary[section_n]) - 1].append([i, segmented_areas[section_n][i][i0][1], segmented_areas[section_n][i][i0][2]]) # [i, left, right]
                            i0 = i0 + 1
                    i = i + 1
                    break
                else:
                    i = i + 1
            
            while (i < len(segmented_areas[section_n])):
                i0 = 2
                while (i0 < len(segmented_areas[section_n][i])):
                    if segmented_areas[section_n][i][i0][0] > 0:
                        break
                    else:
                        section_boundary[section_n][len(section_boundary[section_n]) - 1].append([i, segmented_areas[section_n][i][i0][1], segmented_areas[section_n][i][i0][2]]) # [i, left, right]
                        i0 = i0 + 1
                i = i + 1
            
            i = 0 # bottom boundary -> 1
            while (i < len(segmented_areas[section_n])):
                flag1 = 0 # 1 if any section is present in boundary
                i0 = len(segmented_areas[section_n][i]) - 1
                while (i0 > 1):
                    if segmented_areas[section_n][i][i0][0] < x_length:
                        break
                    else:
                        section_boundary[section_n].append([1,[i, segmented_areas[section_n][i][i0][1], segmented_areas[section_n][i][i0][2]]]) # [i, left, right]
                        flag1 = 1
                        i0 = i0 - 1
                        break
                
                if flag1 == 1:
                    while (i0 > 1):
                        if segmented_areas[section_n][i][i0][0] < x_length:
                            break
                        else:
                            section_boundary[section_n][len(section_boundary[section_n]) - 1].append([i, segmented_areas[section_n][i][i0][1], segmented_areas[section_n][i][i0][2]]) # [i, left, right]
                            i0 = i0 - 1
                    i = i + 1
                    break
                else:
                    i = i + 1

            while (i < len(segmented_areas[section_n])):
                i0 = len(segmented_areas[section_n][i]) - 1
                while (i0 > 1):
                    if segmented_areas[section_n][i][i0][0] < x_length:
                        break
                    else:
                        section_boundary[section_n][len(section_boundary[section_n]) - 1].append([i, segmented_areas[section_n][i][i0][1], segmented_areas[section_n][i][i0][2]]) # [i, left, right]
                        i0 = i0 - 1
                i = i + 1
            
            flag1 = 0 # 1 if any section is present in boundary
            temp2 = 0 # index of one section in boundary
            i = 0 # left boundary -> 2
            while (i < len(segmented_areas[section_n])):
                i0 = 2
                while (i0 < len(segmented_areas[section_n][i])):
                    if segmented_areas[section_n][i][i0][1] == 0:
                        section_boundary[section_n].append([2,[i, segmented_areas[section_n][i][i0][0]]])
                        temp1 = segmented_areas[section_n][i][i0][0]
                        temp2 = len(section_boundary[section_n][len(section_boundary[section_n]) - 1]) - 1
                        temp3 = segmented_areas[section_n][i][i0][0]
                        i1 = i0 + 1
                        while (i1 < len(segmented_areas[section_n][i])):
                            if segmented_areas[section_n][i][i1][0] > temp3 + 1:
                                break
                            elif segmented_areas[section_n][i][i1][1] == 0:
                                temp1 = segmented_areas[section_n][i][i1][0]
                                temp3 = temp3 + 1
                            i1 = i1 + 1
                        section_boundary[section_n][len(section_boundary[section_n]) - 1][temp2].append(temp1)
                        flag1 = 1
                        i0 = i1
                        break
                    else:
                        i0 = i0 + 1
                
                if flag1 == 1:
                    while (i0 < len(segmented_areas[section_n][i])):
                        if segmented_areas[section_n][i][i0][1] == 0:
                            section_boundary[section_n][len(section_boundary[section_n]) - 1].append([i, segmented_areas[section_n][i][i0][0]])
                            temp1 = segmented_areas[section_n][i][i0][0]
                            temp2 = len(section_boundary[section_n][len(section_boundary[section_n]) - 1]) - 1
                            temp3 = segmented_areas[section_n][i][i0][0]
                            i1 = i0 + 1
                            while (i1 < len(segmented_areas[section_n][i])):
                                if segmented_areas[section_n][i][i1][0] > temp3 + 1:
                                    break
                                elif segmented_areas[section_n][i][i1][1] == 0:
                                    temp1 = segmented_areas[section_n][i][i1][0]
                                    temp3 = temp3 + 1
                                i1 = i1 + 1
                            section_boundary[section_n][len(section_boundary[section_n]) - 1][temp2].append(temp1)
                            i0 = i1
                        else:
                            i0 = i0 + 1
                    i = i + 1
                    break
                else:
                    i = i + 1

            while (i < len(segmented_areas[section_n])):
                i0 = 2
                while (i0 < len(segmented_areas[section_n][i])):
                    if segmented_areas[section_n][i][i0][1] == 0:
                        section_boundary[section_n][len(section_boundary[section_n]) - 1].append([i, segmented_areas[section_n][i][i0][0]])
                        temp1 = segmented_areas[section_n][i][i0][0]
                        temp2 = len(section_boundary[section_n][len(section_boundary[section_n]) - 1]) - 1
                        temp3 = segmented_areas[section_n][i][i0][0]
                        i1 = i0 + 1
                        while (i1 < len(segmented_areas[section_n][i])):
                            if segmented_areas[section_n][i][i1][0] > temp3 + 1:
                                break
                            elif segmented_areas[section_n][i][i1][1] == 0:
                                temp1 = segmented_areas[section_n][i][i1][0]
                                temp3 = temp3 + 1
                            i1 = i1 + 1
                        section_boundary[section_n][len(section_boundary[section_n]) - 1][temp2].append(temp1)
                        i0 = i1
                    else:
                        i0 = i0 + 1
                i = i + 1
            
            flag1 = 0 # 1 if any section is present in boundary
            temp2 = 0 # index of one section in boundary
            i = 0 # right boundary -> 3
            while (i < len(segmented_areas[section_n])):
                i0 = len(segmented_areas[section_n][i]) - 1
                while (i0 > 1):
                    if segmented_areas[section_n][i][i0][2] == y_length:
                        section_boundary[section_n].append([3,[i, segmented_areas[section_n][i][i0][0]]])
                        temp1 = segmented_areas[section_n][i][i0][0]
                        temp2 = len(section_boundary[section_n][len(section_boundary[section_n]) - 1]) - 1
                        temp3 = segmented_areas[section_n][i][i0][0]
                        i1 = i0 - 1
                        while (i1 > 1):
                            if segmented_areas[section_n][i][i1][0] < temp3 - 1:
                                break
                            elif segmented_areas[section_n][i][i1][2] == y_length:
                                temp1 = segmented_areas[section_n][i][i1][0]
                                temp3 = temp3 - 1
                            i1 = i1 - 1
                        section_boundary[section_n][len(section_boundary[section_n]) - 1][temp2].insert(1,temp1)
                        flag1 = 1
                        i0 = i1
                        break
                    else:
                        i0 = i0 - 1
                
                if flag1 == 1:
                    while (i0 > 1):
                        if segmented_areas[section_n][i][i0][2] == y_length:
                            section_boundary[section_n][len(section_boundary[section_n]) - 1].append([i, segmented_areas[section_n][i][i0][0]])
                            temp1 = segmented_areas[section_n][i][i0][0]
                            temp2 = len(section_boundary[section_n][len(section_boundary[section_n]) - 1]) - 1
                            temp3 = segmented_areas[section_n][i][i0][0]
                            i1 = i0 - 1
                            while (i1 > 1):
                                if segmented_areas[section_n][i][i1][0] < temp3 - 1:
                                    break
                                elif segmented_areas[section_n][i][i1][2] == y_length:
                                    temp1 = segmented_areas[section_n][i][i1][0]
                                    temp3 = temp3 - 1
                                i1 = i1 - 1
                            section_boundary[section_n][len(section_boundary[section_n]) - 1][temp2].insert(1,temp1)
                            i0 = i1
                        else:
                            i0 = i0 - 1
                    i = i + 1
                    break
                else:
                    i = i + 1

            while (i < len(segmented_areas[section_n])):
                i0 = len(segmented_areas[section_n][i]) - 1
                while (i0 > 1):
                    if segmented_areas[section_n][i][i0][2] == y_length:
                        section_boundary[section_n][len(section_boundary[section_n]) - 1].append([i, segmented_areas[section_n][i][i0][0]])
                        temp1 = segmented_areas[section_n][i][i0][0]
                        temp2 = len(section_boundary[section_n][len(section_boundary[section_n]) - 1]) - 1
                        temp3 = segmented_areas[section_n][i][i0][0]
                        i1 = i0 - 1
                        while (i1 > 1):
                            if segmented_areas[section_n][i][i1][0] < temp3 - 1:
                                break
                            elif segmented_areas[section_n][i][i1][2] == y_length:
                                temp1 = segmented_areas[section_n][i][i1][0]
                                temp3 = temp3 - 1
                            i1 = i1 - 1
                        section_boundary[section_n][len(section_boundary[section_n]) - 1][temp2].insert(1,temp1)
                        i0 = i1
                    else:
                        i0 = i0 - 1
                i = i + 1    

    # combine segments across sections
    combine_seg_sec = []
    for section_n in range(len(section_boundary)):
        if len(section_boundary[section_n]) > 0:
            for j in range(1,len(section_boundary[section_n])):
                if section_boundary[section_n][j][0] == 2:
                    # section_n - 1
                    if section_n % x_total != 0: # == 0 indicates leftmost section
                        for i in range(1,len(section_boundary[section_n - 1])):
                            if section_boundary[section_n - 1][i][0] == 3:
                                j1 = 1
                                while (j1 < len(section_boundary[section_n][j])):
                                    i1 = 1
                                    while (i1 < len(section_boundary[section_n - 1][i])):
                                        if section_boundary[section_n - 1][i][i1][1] <= section_boundary[section_n][j][j1][1] and section_boundary[section_n - 1][i][i1][2] >= section_boundary[section_n][j][j1][1]:
                                            combine_seg_sec.append([[section_n, section_boundary[section_n][j][0], section_boundary[section_n][j][j1]], [section_n - 1, section_boundary[section_n - 1][i][0], section_boundary[section_n - 1][i][i1]]])
                                        elif section_boundary[section_n][j][j1][1] <= section_boundary[section_n - 1][i][i1][1] and section_boundary[section_n][j][j1][2] >= section_boundary[section_n - 1][i][i1][1]:
                                            combine_seg_sec.append([[section_n, section_boundary[section_n][j][0], section_boundary[section_n][j][j1]], [section_n - 1, section_boundary[section_n - 1][i][0], section_boundary[section_n - 1][i][i1]]])
                                        i1 = i1 + 1
                                    j1 = j1 + 1
                                break
                elif section_boundary[section_n][j][0] == 3:
                    # section_n + 1
                    if (section_n + 1) % x_total != 0: # == 0 indicates rightmost section
                        for i in range(1,len(section_boundary[section_n + 1])):
                            if section_boundary[section_n + 1][i][0] == 2:
                                j1 = 1
                                while (j1 < len(section_boundary[section_n][j])):
                                    i1 = 1
                                    while (i1 < len(section_boundary[section_n + 1][i])):
                                        if section_boundary[section_n + 1][i][i1][1] <= section_boundary[section_n][j][j1][1] and section_boundary[section_n + 1][i][i1][2] >= section_boundary[section_n][j][j1][1]:
                                            combine_seg_sec.append([[section_n, section_boundary[section_n][j][0], section_boundary[section_n][j][j1]], [section_n + 1, section_boundary[section_n + 1][i][0], section_boundary[section_n + 1][i][i1]]])
                                        elif section_boundary[section_n][j][j1][1] <= section_boundary[section_n + 1][i][i1][1] and section_boundary[section_n][j][j1][2] >= section_boundary[section_n + 1][i][i1][1]:
                                            combine_seg_sec.append([[section_n, section_boundary[section_n][j][0], section_boundary[section_n][j][j1]], [section_n + 1, section_boundary[section_n + 1][i][0], section_boundary[section_n + 1][i][i1]]])
                                        i1 = i1 + 1
                                    j1 = j1 + 1
                                break
                elif section_boundary[section_n][j][0] == 0:
                    # section_n - x_total
                    if (section_n - x_total) >= 0:
                        for i in range(1,len(section_boundary[section_n - x_total])):
                            if section_boundary[section_n - x_total][i][0] == 1:
                                j1 = 1
                                while (j1 < len(section_boundary[section_n][j])):
                                    i1 = 1
                                    while (i1 < len(section_boundary[section_n - x_total][i])):
                                        if section_boundary[section_n - x_total][i][i1][1] <= section_boundary[section_n][j][j1][1] and section_boundary[section_n - x_total][i][i1][2] >= section_boundary[section_n][j][j1][1]:
                                            combine_seg_sec.append([[section_n, section_boundary[section_n][j][0], section_boundary[section_n][j][j1]], [section_n - x_total, section_boundary[section_n - x_total][i][0], section_boundary[section_n - x_total][i][i1]]])
                                        elif section_boundary[section_n][j][j1][1] <= section_boundary[section_n - x_total][i][i1][1] and section_boundary[section_n][j][j1][2] >= section_boundary[section_n - x_total][i][i1][1]:
                                            combine_seg_sec.append([[section_n, section_boundary[section_n][j][0], section_boundary[section_n][j][j1]], [section_n - x_total, section_boundary[section_n - x_total][i][0], section_boundary[section_n - x_total][i][i1]]])
                                        i1 = i1 + 1
                                    j1 = j1 + 1
                                break
                else:
                    # section_n + x_total
                    if (section_n + x_total) <= (x_total * y_total) - 1:
                        for i in range(1,len(section_boundary[section_n + x_total])):
                            if section_boundary[section_n + x_total][i][0] == 0:
                                j1 = 1
                                while (j1 < len(section_boundary[section_n][j])):
                                    i1 = 1
                                    while (i1 < len(section_boundary[section_n + x_total][i])):
                                        if section_boundary[section_n + x_total][i][i1][1] <= section_boundary[section_n][j][j1][1] and section_boundary[section_n + x_total][i][i1][2] >= section_boundary[section_n][j][j1][1]:
                                            combine_seg_sec.append([[section_n, section_boundary[section_n][j][0], section_boundary[section_n][j][j1]], [section_n + x_total, section_boundary[section_n + x_total][i][0], section_boundary[section_n + x_total][i][i1]]])
                                        elif section_boundary[section_n][j][j1][1] <= section_boundary[section_n + x_total][i][i1][1] and section_boundary[section_n][j][j1][2] >= section_boundary[section_n + x_total][i][i1][1]:
                                            combine_seg_sec.append([[section_n, section_boundary[section_n][j][0], section_boundary[section_n][j][j1]], [section_n + x_total, section_boundary[section_n + x_total][i][0], section_boundary[section_n + x_total][i][i1]]])
                                        i1 = i1 + 1
                                    j1 = j1 + 1
                                break
    
    final_seg_sec = []
    combine_seg_sec_covered = []
    for i in range(len(combine_seg_sec)):
        combine_seg_sec_covered.append(0)

    # sequentially combine the combine_seg_sec groups
    i1 = 0
    while (i1 < len(combine_seg_sec)):
        temp1 = 0
        final_seg_sec.append([[combine_seg_sec[i1][0][0], combine_seg_sec[i1][0][2][0]], [combine_seg_sec[i1][1][0], combine_seg_sec[i1][1][2][0]]])
        i2 = i1 + 1
        while (i2 < len(combine_seg_sec)):
            if combine_seg_sec[i1][0][0] == combine_seg_sec[i2][0][0] and combine_seg_sec[i1][0][2][0] == combine_seg_sec[i2][0][2][0]:
                final_seg_sec[len(final_seg_sec) - 1].append([combine_seg_sec[i2][0][0], combine_seg_sec[i2][0][2][0]])
                final_seg_sec[len(final_seg_sec) - 1].append([combine_seg_sec[i2][1][0], combine_seg_sec[i2][1][2][0]])
                temp1 = 1
            elif combine_seg_sec[i1][1][0] == combine_seg_sec[i2][0][0] and combine_seg_sec[i1][1][2][0] == combine_seg_sec[i2][0][2][0]:
                final_seg_sec[len(final_seg_sec) - 1].append([combine_seg_sec[i2][0][0], combine_seg_sec[i2][0][2][0]])
                final_seg_sec[len(final_seg_sec) - 1].append([combine_seg_sec[i2][1][0], combine_seg_sec[i2][1][2][0]])
                temp1 = 1
            if combine_seg_sec[i1][0][0] == combine_seg_sec[i2][1][0] and combine_seg_sec[i1][0][2][0] == combine_seg_sec[i2][1][2][0]:
                final_seg_sec[len(final_seg_sec) - 1].append([combine_seg_sec[i2][0][0], combine_seg_sec[i2][0][2][0]])
                final_seg_sec[len(final_seg_sec) - 1].append([combine_seg_sec[i2][1][0], combine_seg_sec[i2][1][2][0]])
                temp1 = 1
            elif combine_seg_sec[i1][1][0] == combine_seg_sec[i2][1][0] and combine_seg_sec[i1][1][2][0] == combine_seg_sec[i2][1][2][0]:
                final_seg_sec[len(final_seg_sec) - 1].append([combine_seg_sec[i2][0][0], combine_seg_sec[i2][0][2][0]])
                final_seg_sec[len(final_seg_sec) - 1].append([combine_seg_sec[i2][1][0], combine_seg_sec[i2][1][2][0]])
                temp1 = 1
            if temp1 == 1:
                combine_seg_sec_covered[i2] = 1
            i2 = i2 + 1
        i1 = i1 + 1
    
    i = 0
    while (i < len(final_seg_sec)):
        i1 = 0
        while (i1 < len(final_seg_sec[i])):
            i2 = i1 + 1
            while (i2 < len(final_seg_sec[i])):
                if final_seg_sec[i][i1] == final_seg_sec[i][i2]:
                    del final_seg_sec[i][i2]
                else:
                    i2 = i2 + 1
            i1 = i1 + 1
        i = i + 1
    
    #identify and append the combine_seg_sec groups which are not covered 
    flag1 = 0
    while (flag1 == 0):
        i1 = 0
        temp2 = 0
        while (i1 < len(combine_seg_sec)):
            if combine_seg_sec_covered[i1] == 0:
                temp1 = 0
                j1 = 0
                while (j1 < len(final_seg_sec)):
                    j2 = 0
                    while (j2 < len(final_seg_sec[j1])):
                        if combine_seg_sec[i1][0][0] == final_seg_sec[j1][j2][0] and combine_seg_sec[i1][0][2][0] == final_seg_sec[j1][j2][1]:
                            final_seg_sec[j1].append([combine_seg_sec[i1][0][0], combine_seg_sec[i1][0][2][0]])
                            final_seg_sec[j1].append([combine_seg_sec[i1][1][0], combine_seg_sec[i1][1][2][0]])
                            temp1 = 1
                            temp2 = 1
                            combine_seg_sec_covered[i1] = temp1
                            break
                        elif combine_seg_sec[i1][1][0] == final_seg_sec[j1][j2][0] and combine_seg_sec[i1][1][2][0] == final_seg_sec[j1][j2][1]:
                            final_seg_sec[j1].append([combine_seg_sec[i1][0][0], combine_seg_sec[i1][0][2][0]])
                            final_seg_sec[j1].append([combine_seg_sec[i1][1][0], combine_seg_sec[i1][1][2][0]])
                            temp1 = 1
                            temp2 = 1
                            combine_seg_sec_covered[i1] = temp1
                            break
                        j2 = j2 + 1
                    if temp1 == 1:
                        break
                    j1 = j1 + 1                
            i1 = i1 + 1
        if temp2 == 0:
            flag1 = 1
        
        i = 0
        while (i < len(final_seg_sec)):
            i1 = 0
            while (i1 < len(final_seg_sec[i])):
                i2 = i1 + 1
                while (i2 < len(final_seg_sec[i])):
                    if final_seg_sec[i][i1] == final_seg_sec[i][i2]:
                        del final_seg_sec[i][i2]
                    else:
                        i2 = i2 + 1
                i1 = i1 + 1
            i = i + 1
    
    combine_seg_sec = []

    # combine the related final_seg_sec groups
    flag1 = 0
    while (flag1 == 0):
        temp2 = 0
        i = 0
        while (i < len(final_seg_sec)):
            j = i + 1
            while (j < len(final_seg_sec)):
                temp1 = 0
                j1 = 0
                while (j1 < len(final_seg_sec[j])):
                    if final_seg_sec[i].__contains__(final_seg_sec[j][j1]) == True:
                        j2 = 0
                        while (j2 < len(final_seg_sec[j])):
                            final_seg_sec[i].append(final_seg_sec[j][j2])
                            j2 = j2 + 1
                        temp1 = 1
                        temp2 = 1
                        break
                    j1 = j1 + 1
                if temp1 == 1:
                    del final_seg_sec[j]
                else:
                    j = j + 1
            i = i + 1
        if temp2 == 0:
            flag1 = 1

        i = 0
        while (i < len(final_seg_sec)):
            i1 = 0
            while (i1 < len(final_seg_sec[i])):
                i2 = i1 + 1
                while (i2 < len(final_seg_sec[i])):
                    if final_seg_sec[i][i1] == final_seg_sec[i][i2]:
                        del final_seg_sec[i][i2]
                    else:
                        i2 = i2 + 1
                i1 = i1 + 1
            i = i + 1

    i = 0
    while (i < len(final_seg_sec)):
        i1 = 0
        while (i1 < len(final_seg_sec[i])):
            i2 = i1 + 1
            while (i2 < len(final_seg_sec[i])):
                if final_seg_sec[i][i1] == final_seg_sec[i][i2]:
                    del final_seg_sec[i][i2]
                else:
                    i2 = i2 + 1
            i1 = i1 + 1
        i = i + 1
    
    section_boundary = []
    
    combined_areas = [] # combine areas as per final_seg_sec
    """for line in final_seg_sec:
        combined_areas.append([])
        temp1 = len(combined_areas) - 1
        temp2 = -1
        for line1 in line:
            combined_areas[temp1].append([line1])
            temp2 = temp2 + 1
            temp3 = len(segmented_areas[line1[0]][line1[1]])
            for i in range(2,temp3):
                if len(segmented_areas[line1[0]][line1[1]][i]) == 3:
                    combined_areas[temp1][temp2].append(segmented_areas[line1[0]][line1[1]][i])
            segmented_areas[line1[0]][line1[1]].append([-1])"""

    #print(segmented_areas[2])
    i1 = 0
    temp1 = len(segmented_areas)
    while (i1 < temp1):
        i2 = 0
        while (i2 < len(segmented_areas[i1])):
            if segmented_areas[i1][i2][len(segmented_areas[i1][i2]) - 1] == [-1]:
                del segmented_areas[i1][i2]
            else:
                i2 = i2 + 1
        i1 = i1 + 1
    
    # apply colors
    for section_n in range(len(section_items)):
        i1 = 0
        while (i1 < len(segmented_areas[section_n])):
            random_colorR = random.randint(40,255)
            random_colorG = random.randint(40,255)
            random_colorB = random.randint(40,255)
            i2 = 2
            while (i2 < len(segmented_areas[section_n][i1])):
                i = segmented_areas[section_n][i1][i2][1]
                while (i <= segmented_areas[section_n][i1][i2][2]):
                    section_items[section_n][segmented_areas[section_n][i1][i2][0]][i][0] = random_colorR
                    section_items[section_n][segmented_areas[section_n][i1][i2][0]][i][1] = random_colorG
                    section_items[section_n][segmented_areas[section_n][i1][i2][0]][i][2] = random_colorB
                    i = i + 1
                i2 = i2 + 1
            i1 = i1 + 1

    for section_n in range(len(combined_areas)):
        random_colorR = random.randint(40,255)
        random_colorG = random.randint(40,255)
        random_colorB = random.randint(40,255)
        i1 = 0
        while (i1 < len(combined_areas[section_n])):
            i2 = 1 # doubtful
            while (i2 < len(combined_areas[section_n][i1])):
                i = combined_areas[section_n][i1][i2][1]
                while (i <= combined_areas[section_n][i1][i2][2]):
                    section_items[combined_areas[section_n][i1][0][0]][combined_areas[section_n][i1][i2][0]][i][0] = random_colorR
                    section_items[combined_areas[section_n][i1][0][0]][combined_areas[section_n][i1][i2][0]][i][1] = random_colorG
                    section_items[combined_areas[section_n][i1][0][0]][combined_areas[section_n][i1][i2][0]][i][2] = random_colorB
                    i = i + 1
                i2 = i2 + 1
            i1 = i1 + 1

    # arrange sections as per original order for display
    section_items_final = []
    j1 = 0
    i = 0
    while (j1 < y_total):
        j = 0
        while (j < s_size):
            if i < y_axis:
                section_items_final.append([])
                j2 = 0
                while (j2 < x_total):
                    i1 = 0
                    while (i1 < len(section_items[(j1 * x_total) + j2][j])):
                        section_items_final[i].append(section_items[(j1 * x_total) + j2][j][i1])
                        i1 = i1 + 1
                    j2 = j2 + 1
                j = j + 1
                i = i + 1
            else:
                break
        j1 = j1 + 1
    
    print('len',len(section_items_final))
    viewer = skimage.viewer.ImageViewer(np.array(section_items_final))
    viewer.show()
    
    """#output_file_open = open('white_groups_combined.csv', 'w', newline='', encoding='utf16')
    #csv_write1 = csv.writer(output_file_open, delimiter = ',')
    #output_file_open = open('white_groups_segmented.csv', 'w', newline='', encoding='utf16')
    #csv_write2 = csv.writer(output_file_open, delimiter = ',')
    
    # write to csv file
    for i in combined_areas:
        for i1 in i:
            for i2 in i1:
                csv_write1.writerow(i2)
        csv_write1.writerow('')
    for i in segmented_areas:
        for i1 in i:
            for i2 in i1:
                csv_write2.writerow(i2)
        csv_write2.writerow('')
    return 0"""

white_segments(y_axis, x_axis, s_size)
