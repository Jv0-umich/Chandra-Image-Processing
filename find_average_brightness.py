#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 12:02:32 2021

@author: javierguerrero
"""
import sys
from Header import determine_center
from Header import plot_box
from Header import radial_profile
from Header import sub_mean_brightness
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.table import Table
from matplotlib.colors import LogNorm
import numpy as np
obsid = sys.argv[1]
input_x = sys.argv[2]
input_y = sys.argv[3]
width = sys.argv[4]
immin = sys.argv[5]
immax = sys.argv[6]
width = float(width)
immin = float(immin)
immax = float(immax)


DATADIR = "/Users/javierguerrero/code/Urop/images/"
image_url = DATADIR + obsid + "_evt2.fits"
image_save = DATADIR + "/" + obsid + obsid + "_evt2.fits"

input_x = float(input_x)
input_y = float(input_y)
xmid , ymid = determine_center(image_url, input_x, input_y, .05, 100)
xmid , ymid = determine_center(image_url, xmid, ymid, .05, 10)


ii = plot_box(image_url, xmid, ymid, 10, c_line = True)

plt.clf()

midpoints, results = radial_profile(xmid, ymid, image_url)




hdu_list = fits.open(image_url, memmap=True)
evt_data = Table(hdu_list[1].data)
NBINS = (100,100)


ii = (evt_data['ccd_id'] == 7) & (evt_data['x'] < xmid + width) & (evt_data['x'] > xmid - width) & (evt_data['y'] > ymid - width) & (evt_data['y'] < ymid + width)
    
h, xedge, yedge, image = plt.hist2d(evt_data['x'][ii], evt_data['y'][ii], NBINS, cmap='viridis', norm=LogNorm()) #removed assigment

SBmean, xx, yy, rr, gridpoints = sub_mean_brightness(xmid, ymid, midpoints, results, image_url, xedge, yedge)

plt.clf()
image1 = np.subtract(h ,SBmean.T)

#plt.imshow(SBmean, norm=LogNorm())

plt.imshow(image1, vmin= immin, vmax= immax, origin = 'lower')
plt.colorbar()


plt.xlabel('x')
plt.ylabel('y')

plt.savefig(obsid + "_sub_image.png")















