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

RBINS = np.append(np.linspace(0, 20, 40), np.logspace(np.log10(21), np.log10(500), 960))

def plot_star(x_min, x_max, y_min, y_max, file_url, ccd_id_num=7, is_default=False): 
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
    if(is_default):
        plt.hist2d(evt_data['x'][ii], evt_data['y'][ii], NBINS, cmap='viridis', norm=LogNorm()) #removed assigment
        
        cbar = plt.colorbar(ticks=[1.0,3.0,6.0])
        cbar.ax.set_yticklabels(['1','3','6'])

        plt.xlabel('x')
        plt.ylabel('y')

    return ii


def plot_box(file_url, xcenter, ycenter, box_width=10, ccd_id_num = 7, is_default = False, c_line = False):
	
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
    
    if (c_line & is_default):
        
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
    rx = 10.0
    
    
    while rx > perror:
        
        ii = plot_box(file_url= file_url, xcenter = xmid0, ycenter = ymid0, box_width = boxw)
        xmid = np.median(evt_data['x'][ii])
        ymid = np.median(evt_data['y'][ii])
        
        #rx = (xmid0-xmid)/xmid0
        #ry = (ymid0-ymid)/ymid0
        rx  = np.sqrt((xmid0 - xmid)**2 + (ymid0 - ymid)**2)
        if rx < perror :#and ry < perror:
            return xmid,ymid
        else:
            xmid0 = xmid
            ymid0 = ymid

def radial_profile(xmid, ymid, file_url,R_bin = RBINS):
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
    hdu_list = fits.open(file_url, memmap=True)
    evt_data = Table(hdu_list[1].data)
    
    result = []
    midpoints = []
    R = np.sqrt((evt_data['x']- xmid)**2 + (evt_data['y'] - ymid)**2)
    
    for j in range(len(R_bin)-1):
    
        i = (R>=R_bin[j]) & (R<R_bin[j+1])
        
        midpoints.append((R_bin[j] + R_bin[j+1]) / 2)
        
        area = np.pi*((R_bin[j+1])**2 - (R_bin[j])**2)
    
        result.append(len(R[i])/area)
    return np.array(midpoints),np.array(result)
    
    
def sub_mean_brightness(xmid, ymid, midpoints, surfbright, file_url, xedges, yedges, width = 500):
    
    
    negative = [element * -1 for element in midpoints]
    gridmidpoints = np.concatenate((negative,midpoints))
    
    xx, yy = np.meshgrid((xedges[:-1] + xedges[1:])/2,
                         (yedges[:-1] + yedges[1:])/2)
    
    rr = np.sqrt( (xx - xmid)**2 + (yy - ymid)**2 )
    
    area = (xedges[1] - xedges[0]) * (yedges[1] - yedges[0])
    
    SBmean = np.interp(rr, midpoints, surfbright)*area
    
    return SBmean, xx, yy, rr, gridmidpoints
    
    
























