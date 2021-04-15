#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 12:02:32 2021

@author: javierguerrero
"""
import sys
import numpy as np
from astropy.io import fits
from astropy.table import Table
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
DATADIR = sys.argv[1]
obsid = sys.argv[2]
input_x = sys.argv[3]
input_y = sys.argv[4]

image_url = DATADIR + obsid + "_evt2.fits"

input_x = float(input_x)
input_y = float(input_y)
x_mid = 0
y_mid = 0


hdu_list = fits.open(image_url, memmap=True)
evt_data = Table(hdu_list[1].data)
ii = (evt_data['ccd_id'] == 7)
NBINS = (100,100)
plt.hist2d(evt_data['x'][ii], evt_data['y'][ii], NBINS, norm=LogNorm()) #removed assigment
cbar = plt.colorbar(ticks=[1.0,3.0,6.0])
cbar.ax.set_yticklabels(['1','3','6'])
    
plt.savefig(obsid + "_full_image.png")


