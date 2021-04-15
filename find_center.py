#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 12:02:32 2021

@author: javierguerrero
"""
import sys
from Header import determine_center
from Header import plot_box
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
x_mid , y_mid = determine_center(image_url, input_x, input_y, .05, 100)
x_mid , y_mid = determine_center(image_url, input_x, input_y, .05, 10)


ii = plot_box(image_url, x_mid, y_mid, 10, c_line = True, is_default = True)

plt.savefig(obsid + "_center_image.png")

print(x_mid, y_mid)
