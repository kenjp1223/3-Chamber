# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 17:28:14 2018
Track black object from video.
@author: owner
"""

import numpy as np    #libarary for list manipulations
import os
import sys  
import matplotlib #library used here for plotting
import matplotlib.pyplot as plt
matplotlib.use('WXAgg')
import pandas as pd
import cv2


def track_object(VIDEO,RESULTS,TRACK,ZERO_IMAGE,NAME,THRESH = 20):
    INTERVAL = 33
    ESC_KEY = 0x1b
    
    count = 0
    fps = VIDEO.get(cv2.CAP_PROP_FPS)
    time_frame = count/fps
    end_flag,c_frame = VIDEO.read()
    h, w, channels = c_frame.shape
    g_frame_zero = cv2.cvtColor(c_frame, cv2.COLOR_BGR2GRAY)
    backtorgb_zero = cv2.cvtColor(g_frame_zero,cv2.COLOR_GRAY2RGB)
    x = [0]
    y = [0]
    Time = [0]
    Track = np.zeros_like(c_frame)
    shamTrack = np.zeros_like(c_frame)

    while end_flag == True:
        # グレースケール変換
        g_frame = cv2.cvtColor(c_frame, cv2.COLOR_BGR2GRAY)
        # 0 frame imageとの差分を取る
        img_diff = 255 - cv2.absdiff(g_frame,g_frame_zero)
        #img_diff = cv2.medianBlur(g_frame,21) # alternative approach
        #cv2.imshow("Difference",img_diff) # For debug
        # 二値化
        ret,th1 = cv2.threshold(g_frame,THRESH,255,cv2.THRESH_BINARY)
        # Filter
        th1 = cv2.medianBlur(th1,21)      
        #cv2.imshow("blur",th1) # For debug
        
        #backtorgb = cv2.cvtColor(th1,cv2.COLOR_GRAY2RGB)
        backtorgb_g = cv2.cvtColor(g_frame,cv2.COLOR_GRAY2RGB)
        
        #get contours
        image, contours, hierarchy = cv2.findContours(255-th1,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        
        #Detect black object
        max_area = 0
        j = 0
        if len(contours) != 0:           
            for j in range(len(contours)):
                area = cv2.contourArea(contours[j])
                if max_area < area:
                    max_area = area
                    max_area_contours = j
            cnt = contours[max_area_contours]
            M = cv2.moments(cnt)
            if M['m00'] == 0:
                x_frame = x[-1]
                y_frame = y[-1]
            else:
                x_frame = int(M['m10']/M['m00'])
                y_frame = int(M['m01']/M['m00'])
        else:
            x_frame = x[-1]
            y_frame = y[-1]
        #if video taken in red light, use backtorgb instead of c_frame
        frame = cv2.drawContours(backtorgb_g, contours, -1, (0,255,0), 3)
        frame = cv2.circle(frame,(x_frame,y_frame), 5, (255,255,255), -1)
        #for debug
        #cv2.imshow(NAME + ' contour',frame)
        
        if len(x) == 1:
            Track = cv2.line(Track, (x_frame,y_frame), (x_frame,y_frame),(0,153,244), 1,cv2.LINE_AA)
            shamTrack = cv2.line(shamTrack, (x_frame,y_frame), (x_frame,y_frame),(0,153,244), 1,cv2.LINE_AA)
        else:
            Track = cv2.line(Track, (x_frame,y_frame), (x[-1],y[-1]),(0,153,244), 1,cv2.LINE_AA)
            shamTrack = cv2.line(shamTrack, (x_frame,y_frame), (x[-1],y[-1]),(0,153,244), 1,cv2.LINE_AA)  
        x = np.append(x, x_frame)
        y = np.append(y, y_frame)
        Time = np.append(Time,time_frame)
        #cv2.imshow("track of " + ORG_FILE_NAME, imgTrack)
        imgTrack = cv2.addWeighted(backtorgb_g,0.5,Track,1,0.)
        
        #cv2.imshow(NAME,img_diff)# For debug
        #cv2.imshow(NAME + 'track', imgTrack)# For debug
        count = count + 1
        time_frame = count/fps

        # フレーム書き込み
        #rec[rlist.index(i)].write(imgTrack)
        # Escキーで終了
        key = cv2.waitKey(INTERVAL)
        if key == ESC_KEY:
            break
        # 次のフレーム読み込み
        end_flag, c_frame = VIDEO.read()
        
    df = pd.DataFrame({'X':x[1:],'Y':y[1:],'Time (s)':Time[1:]},columns = ['Time (s)','X','Y'])
    #trial = str(rlist.index(i))
    df.to_csv(RESULTS + '\\' + NAME + "_track result.csv",index = False)
    cv2.destroyAllWindows()
    Trace = cv2.addWeighted(backtorgb_zero,0.5,shamTrack,0.8,0.)
    cv2.imwrite(TRACK + '\\' + NAME +' _track.tif',Trace)

    # 終了処理
    #cv2.imwrite(NAME + ' _track.tif',255 - crop_Track)
    #cv2.imwrite(NAME + ' _track1.tif',255 - crop_Track1)
    VIDEO.release()
    #[rec[k].release() for k in range(len(START))]