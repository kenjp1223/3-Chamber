# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 16:25:29 2018
This program crops video to desired length and roi.
@author: owner
"""
import sys
import pandas as pd
import numpy as np
import cv2
import copy
sys.path.append('C:\\Users\\owner\\Desktop\\Python\\Codes')
import get_ROI as GROI


def crop_video(VIDEO,START,LENGTH,OUT,NAME):    
    INTERVAL = 33
    ESC_KEY = 0x1b
    count = 0
    #video1 = cv2.VideoCapture('GCamp 18_1.mp4')
    #end_flag1,c_frame1 = video1.read()
    fps = VIDEO.get(cv2.CAP_PROP_FPS)
    end_flag,c_frame = VIDEO.read()
    r = GROI.get_ROI(c_frame)[0]
    ROI = np.array(r)
    #print(ROI)
    c_frame = c_frame[int(r[2]):int(r[3]), int(r[0]):int(r[1])]  
    zero = copy.copy(c_frame)
    g_frame_zero = cv2.cvtColor(zero, cv2.COLOR_BGR2GRAY)
    backtorgb_zero = cv2.cvtColor(g_frame_zero,cv2.COLOR_GRAY2RGB)
    #c_frame1 = c_frame1[int(r[2]):int(r[3]), int(r[0]):int(r[1])]  
    #g_frame_zero = cv2.cvtColor(c_frame1, cv2.COLOR_BGR2GRAY)
    #backtorgb_zero = cv2.cvtColor(g_frame_zero,cv2.COLOR_GRAY2RGB)     
    h, w, channels = c_frame.shape
    rec = cv2.VideoWriter(OUT+'\\' + NAME +'_crop.mp4',cv2.VideoWriter_fourcc(*'MP4V'),fps, (w, h))
    time_frame = count/fps
    while time_frame < START:
        count = count + 1
        time_frame = count/fps
        end_flag, c_frame = VIDEO.read()
        c_frame = c_frame[int(r[2]):int(r[3]), int(r[0]):int(r[1])]            
    while time_frame < LENGTH  + START:
        #for debug
        #cv2.imshow(NAME,c_frame)
        count = count + 1
        time_frame = count/fps

        # フレーム書き込み
        rec.write(c_frame)
        # Escキーで終了
        key = cv2.waitKey(INTERVAL)
        if key == ESC_KEY:
            break
        # 次のフレーム読み込み
        end_flag, c_frame = VIDEO.read()
        c_frame = c_frame[int(r[2]):int(r[3]), int(r[0]):int(r[1])]    
    cv2.destroyAllWindows()

    # 終了処理
    #cv2.imwrite(OUT + ' _track.png',255 - crop_Track)
    #cv2.imwrite(OUT + ' _track1.png',255 - crop_Track1)
    cv2.destroyAllWindows()
    VIDEO.release()
    rec.release()
    return ROI, backtorgb_zero