#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 15:20:22 2020

@author: javierguerrero
"""

import numpy as np
from astropy.io import fits
from astropy.table import Table
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt


def plot_star(x_min=0, x_max=0, y_min=0, y_max=0, file_url="", ccd_id_num=7, is_default=True):
    hdu_list = fits.open(file_url, memmap=True)
    evt_data = Table(hdu_list[1].data)
    
    ii = (evt_data['ccd_id'] == ccd_id_num) & (evt_data['x'] < x_max) & (evt_data['x'] > x_min) & (evt_data['y'] > y_min) & (evt_data['y'] < y_max)
    


    NBINS = (100,100)
    if(is_default == False):
        img_zero_mpl = plt.hist2d(evt_data['x'][ii], evt_data['y'][ii], NBINS, [[x_min, x_max], [y_min, y_max]], cmap='viridis', norm=LogNorm())
    else:
        img_zero_mpl = plt.hist2d(evt_data['x'][ii], evt_data['y'][ii], NBINS, cmap='viridis', norm=LogNorm())

    cbar = plt.colorbar(ticks=[1.0,3.0,6.0])
    cbar.ax.set_yticklabels(['1','3','6'])

    plt.xlabel('x')
    plt.ylabel('y')

    return ii


def plot_box(file_url, xcenter, ycenter, box_width=10, ccd_id_num = 7, is_default = True):
	
    """
    event_list : FITS table data object that contains the list of events
    xcenter : float : defining the center of your box in sky coordinates (x)
    ycenter : float : defining the center of your box in sky coordinates (x)
    box_width : float : define the width of the box to be plotted (default: 10)
    """
    
    x_min = xcenter - box_width
    x_max = xcenter + box_width
    y_min = ycenter - box_width
    y_max = ycenter + box_width
    
    return plot_star(x_min, x_max, y_min, y_max, file_url, ccd_id_num, is_default)

def determine_center(file_url, xmid0, ymid0, perror, boxw = 10):
    
    hdu_list = fits.open(file_url, memmap=True)
    evt_data = Table(hdu_list[1].data)
    ii = 0
    xmid = 0.0
    ymid = 0.0
    rx = 10.0
    ry = 10.0
    
    while rx > perror and ry > perror:
        ii = plot_box(file_url, xmid0, ymid0, boxw)
    
        xmid = np.median(evt_data['x'][ii])
        ymid = np.median(evt_data['y'][ii])
        
        rx = (xmid0-xmid)/xmid0
        ry = (ymid0-ymid)/ymid0
        if rx < perror and ry < perror:
            return xmid,ymid
        else:
            xmid0 = xmid
            ymid0 = ymid


x_mid , y_mid = determine_center('/Users/javierguerrero/code/spices/6601/primary/acisf06601N002_evt2.fits', 4099.25, 4109, .05)

ii = plot_box('/Users/javierguerrero/code/spices/6601/primary/acisf06601N002_evt2.fits', x_mid, y_mid, 10, is_default=False)


plt.axvline(x_mid, color = 'k')
plt.axhline(y_mid, color = 'r')
    