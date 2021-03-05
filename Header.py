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


def plot_star(x_min=4000, x_max=4200, y_min=4000, y_max=4150, file_url="", ccd_id_num=7, is_default=True):
    """
    
    x_min : float : defining the minimum value of the domain of your graph
    x_max : float : defining the maximum value of the domain of your graph
    y_min : float : defining the minimum value of the range of your graph
    y_max : float : defining the maximum value of the range of your graph
    file_url: event_list : FITS table data object that contains the list of events
    """
    hdu_list = fits.open(file_url, memmap=True)
    evt_data = Table(hdu_list[1].data)
    
    ii = (evt_data['ccd_id'] == ccd_id_num) & (evt_data['x'] < x_max) & (evt_data['x'] > x_min) & (evt_data['y'] > y_min) & (evt_data['y'] < y_max)
    


    NBINS = (100,100)
    if(is_default == True):
        plt.hist2d(evt_data['x'][ii], evt_data['y'][ii], NBINS, cmap='viridis', norm=LogNorm()) #removed assigment
        
        cbar = plt.colorbar(ticks=[1.0,3.0,6.0])
        cbar.ax.set_yticklabels(['1','3','6'])

        plt.xlabel('x')
        plt.ylabel('y')

    return ii


def plot_box(file_url, xcenter, ycenter, box_width=10, ccd_id_num = 7, is_default = True, c_line = False):
	
    """
    file_url: event_list : FITS table data object that contains the list of events
    xcenter : float : defining the center of your box in sky coordinates (x)
    ycenter : float : defining the center of your box in sky coordinates (x)
    box_width : float : define the width of the box to be plotted (default: 10)
    """
    
    x_min = xcenter - box_width
    x_max = xcenter + box_width
    y_min = ycenter - box_width
    y_max = ycenter + box_width
    
    if ((c_line == True) & is_default):
        
        return plot_star(x_min, x_max, y_min, y_max, file_url, ccd_id_num, is_default), plt.axvline(xcenter, color = 'k'), plt.axhline(ycenter, color = 'r')
    
    else:
        return plot_star(x_min, x_max, y_min, y_max, file_url, ccd_id_num, is_default)

def determine_center(file_url, xmid0, ymid0, perror, boxw = 10):
    """
    file_url: event_list : FITS table data object that contains the list of events
    xmid0 : float : defining the estimated center of your box in (x)
    ymid0 : float : defining the estimated center of your box in (y)
    perror : float : define the amount of possible error wanted in determining center
    """
    hdu_list = fits.open(file_url, memmap=True)
    evt_data = Table(hdu_list[1].data)
    ii = 0
    xmid = 0.0
    ymid = 0.0
    rx = 10.0
    ry = 10.0
    
    while rx > perror and ry > perror:
        
        ii = plot_box(file_url, xmid0, ymid0, boxw, is_default = False)
        xmid = np.median(evt_data['x'][ii])
        ymid = np.median(evt_data['y'][ii])
        
        #rx = (xmid0-xmid)/xmid0
        #ry = (ymid0-ymid)/ymid0
        rx  = np.sqrt(pow((xmid0 - xmid), 2) + pow((xmid0 - xmid), 2))
        if rx < perror :#and ry < perror:
            return xmid,ymid
        else:
            xmid0 = xmid
            ymid0 = ymid

def radial_profile(xmid, ymid, ii, R_bin = [1,2,3]):
    """
    Parameters
    ----------
    xmid : float
        X cordinate for center.
    ymid : float
        y cordinate for center.
    ii : Fits table data
        Filtered list of events.
    R_bin : Array, optional
        Bin values for what radial profiles are wanted. The default is [1,2,3].

    Returns
    -------
    array
        Array of values with units photons/pixel^2.

    """
    result = []
    R = np.sqrt(pow(ii.evt_data['x'],2) + pow(ii.evt_data['y'],2))
    
    for j in range(len(R_bin)-1):
    
        i = (R>=R_bin[j]) & (R<R_bin[j+1])
    
        area = np.pi*(pow(R_bin[j+1],2) - pow(R_bin[j],2))
    
        result.append(area/len(R[i]))
    return np.array(result)
    
    
    
    
    


