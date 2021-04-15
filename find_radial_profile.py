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
import matplotlib.pyplot as plt

obsid = sys.argv[1]
input_x = sys.argv[2]
input_y = sys.argv[3]

DATADIR = "/Users/javierguerrero/code/Urop/images/"
image_url = DATADIR + obsid + "_evt2.fits"

input_x = float(input_x)
input_y = float(input_y)
x_mid , y_mid = determine_center(image_url, input_x, input_y, .05, 100)
x_mid , y_mid = determine_center(image_url, x_mid, y_mid, .05, 10)


ii = plot_box(image_url, x_mid, y_mid, 10, c_line = True)

plt.clf()

midpoints, results = radial_profile(x_mid, y_mid, image_url)

plt.plot(midpoints,results)

plt.xlabel('radius (pixels)')
plt.ylabel('surface brightness (counts/pixels^2)')
plt.loglog()

plt.savefig(obsid + "_radial_image.png")
