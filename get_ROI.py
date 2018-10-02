# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 16:36:46 2018

@author: owner
"""


import ctypes    #library used here for handling/accessing dlls
import numpy as np    #libarary for list manipulations
import time
from time import *
import os
import pprint
import random
import csv        #for writing data into csv files
import sys  
import wx         #graphics
import matplotlib #library used here for plotting
import matplotlib.pyplot as plt
matplotlib.use('WXAgg')
from matplotlib.figure import *
from matplotlib.backends.backend_wxagg import *
import pylab
from scipy import interpolate
from scipy import signal
from pylab import *
import pandas as pd
from scipy.signal import butter, lfilter, freqz
import peakutils


from pylab import *
from skimage import data
from skimage.viewer.canvastools import RectangleTool
from skimage.viewer import ImageViewer



def get_rect_coord(extents):
    global viewer,coord_list
    coord_list.append(extents)


def get_ROI(im):
    global viewer,coord_list

    selecting=True
    while selecting:
        viewer = ImageViewer(im)
        coord_list = []
        rect_tool = RectangleTool(viewer, on_enter=get_rect_coord) 
        print("Draw your selections, press ENTER to validate one and close the window when you are finished")
        viewer.show()
        finished= input('Is the selection correct? [y]/n: ')
        if finished!='n':
            selecting=False
    return coord_list