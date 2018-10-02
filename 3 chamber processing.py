# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 16:23:58 2018

@author: owner
"""


import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cv2
import peakutils

sys.path.append('C:\\Users\\owner\\Desktop\\Python\\python3')
import get_ROI as GROI
import crop_video as CROP
import track_object as TOBJ



if __name__ == '__main__':
    DIR = r"C:\Users\owner\Desktop\tests"
    VDIR = DIR + '\\VIDEO'
    OUT = DIR + '\\OUT'
    ZERO = DIR + '\\ZERO'
    ROI = DIR + '\\ROI'
    RESULTS = DIR + '\\RESULTS'
    TRACK = DIR + '\\TRACK'
    
    for xxx in [OUT,ZERO,ROI,RESULTS,TRACK]:
        if not os.path.exists(xxx):
            os.mkdir(xxx)
    
    NAME = 'test'
    VIDEO = cv2.VideoCapture(VDIR + '\\' + NAME +'.avi') # check whether the video is avi or mp4 or something else
    roi,zero = CROP.crop_video(VIDEO,60,600,OUT,NAME)
    
    #save zero image
    plt.imsave(ZERO + '\\' + NAME + '.tif',zero)
    
    #Get roi for stim and control side
    print("Select roi for stim side")
    roi_s = np.array(GROI.get_ROI(zero)[0])
    print("Select roi for control side")
    roi_c = np.array(GROI.get_ROI(zero)[0])
    R = pd.DataFrame({'roi':roi,'stim_side':roi_s,'control_side':roi_c},index=['x1','x2','y1','y2'],\
                       columns=['roi','stim_side','control_side'])
    R.to_csv(ROI + '\\' + NAME + '_roi.csv') #save rois as csv
    
    #Track animal in out_video
    OUT_V = cv2.VideoCapture(OUT + '\\' + NAME +'_crop.mp4')
    TOBJ.track_object(OUT_V,RESULTS,TRACK,zero,NAME)
    