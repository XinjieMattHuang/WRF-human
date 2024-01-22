# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 21:36:51 2022

@author: xh2892
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Script_name: Step5_plottingPSTdata_with_3kmWindVectors
@Created_date: Sep 8 2022
@Author:       Chang Man Hei Jeffrey - HKU Urban Climate and Air Pollution Laboratory
@Version:      1.0

@Plotting area: Whole Hong Kong
@Grid resolution: 10m x 10m
@Domain size: 4800 x 6375

Lines to edit:
1. Line 42  -   # Change to your directory for PST.nc file
2. Line 45  -   # Change to your directory for wrfout.nc file
3. Line 49  -   # Change the Latitude and Longitude of the map extent (if needed)
4. Line 71  -   # Change to your directory for LUM_HKshape.tif
5. Line 118  -   # Change to your directory and graphs output path

6. Line 48  -   # If you want to plot the wind arrows WITH ANOTHER TIMESTAMP from 3km WRF file 
                  Edit "timestamp" in Line 

7. Line 61,64,67,111 and 112  -   # The wind arrows are with 3km resolution and pre-set with the dimension of x=22, y=17 
                                   (Which covering the PST domain from your .nc file)
                                   If you want to include a wider map extent, just to edit:
                                   -> loadwrfout.variables['PARAMETER'][time,70:87,64:86]
                                                                              ^This & ^This
                                                                        y = 70:87 and x = 64:86
"""

import os,glob
import netCDF4 as nc
from netCDF4 import Dataset as NetCDFFile 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage.transform import rescale, resize, downscale_local_mean
#import cartopy.crs as ccrs
from PIL import Image

print('Reading your PST nc file ...')
nc_path = '/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/WRF-HEATS codes/output/Results_10m_2PM_baseline.nc' # Change to calculated PST result nc file
loadnc = nc.Dataset(nc_path,'r')

wrfout_path = '/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/WRF-HEATS codes/output/ACON-wrfout_d03_2016-06-21_00_00_00'
loadwrfout = nc.Dataset(wrfout_path,'r')

timestamp1 = 55
timestamp2 = 79
timestamp3 = 103
timestamp4 = 127
timestamp5 = 151
boundaryLatLong = [22.56172,114.45236,22.14208,113.81551] #North,East,South,West (Lat-Long)

def convert_coordinate(x,y):
    dLat = (boundaryLatLong[2]-boundaryLatLong[0])/480
    dLong = (boundaryLatLong[1]-boundaryLatLong[3])/638
    inputLat = (y - boundaryLatLong[2])/dLat + 480
    inputLong = (x - boundaryLatLong[3])/dLong   
    return (np.array([int(inputLat),int(inputLong)]))

pst_10m = np.array(loadnc.variables['PST'][:,:])
pst_10m_out = pd.DataFrame(pst_10m)  # Select domain extent fitting SLOPE data, you have to identify the extent first

#t2 = np.array(loadwrfout.variables['T2'][timestamp,70:87,64:86]) 
#t2_out = pd.DataFrame(t2)

wind_u1 = np.array(loadwrfout.variables['U10'][timestamp1,70:87,64:86])
wind_u2 = np.array(loadwrfout.variables['U10'][timestamp2,70:87,64:86])
wind_u3 = np.array(loadwrfout.variables['U10'][timestamp3,70:87,64:86])
wind_u4 = np.array(loadwrfout.variables['U10'][timestamp4,70:87,64:86])
wind_u5 = np.array(loadwrfout.variables['U10'][timestamp5,70:87,64:86])
wind_u = (wind_u1 + wind_u2 + wind_u3 + wind_u4 + wind_u5)/5;
wind_u_out = pd.DataFrame(wind_u)

wind_v1 = np.array(loadwrfout.variables['V10'][timestamp1,70:87,64:86])
wind_v2 = np.array(loadwrfout.variables['V10'][timestamp2,70:87,64:86])
wind_v3 = np.array(loadwrfout.variables['V10'][timestamp3,70:87,64:86])
wind_v4 = np.array(loadwrfout.variables['V10'][timestamp4,70:87,64:86])
wind_v5 = np.array(loadwrfout.variables['V10'][timestamp5,70:87,64:86])
wind_v = (wind_v1 + wind_v2 + wind_v3 + wind_v4 + wind_v5)/5;
wind_v_out = pd.DataFrame(wind_v)

print('Reading your land-use shape file ...')
im = Image.open('/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/3. Results - Baseline, PFM, and slopes/plotting codes/LUM_HKshape.tif') # Change to your directory for LUM_HKshape.tif
imarray_10m = pd.DataFrame(np.array(im))
imarray_10m_out = pd.DataFrame(imarray_10m).iloc[::-1,:]

mask_reset = imarray_10m_out==1
mask_reset = mask_reset.reset_index(drop=True)
mask_LUM_land = pst_10m_out[mask_reset]

list_lat = []
list_long = []
delta_boundaryLat = (boundaryLatLong[2]-boundaryLatLong[0])/4800 #Southern boundary - Northern boundary for HK
delta_boundaryLong = (boundaryLatLong[1]-boundaryLatLong[3])/6375 #Eastern boundary - Western boundary for HK
discret_Lat = boundaryLatLong[2]
discret_Long = boundaryLatLong[3]

list_lat.append(format(discret_Lat,'.2f'))
list_long.append(format(discret_Long,'.2f'))

for lat in range(0,4800,960):
    discret_Lat = discret_Lat - delta_boundaryLat*960
    print(discret_Lat)
    list_lat.append(format(discret_Lat,'.2f'))

for long in range(0,6375,1275):
    discret_Long = discret_Long + delta_boundaryLong*1275
    list_long.append(format(discret_Long,'.2f'))
    
    

fig,ax = plt.subplots(figsize=(10,6))
# cs =  plt.imshow(imarray_10m_out, cmap='Greys', aspect='auto',origin='lower', clim=(0,1), alpha=0.5) # You can adjust the range of color bar with clim
cs2 =  plt.imshow(mask_LUM_land , cmap='jet', aspect='auto',origin='lower', alpha=0.5, interpolation='nearest')

cbar = plt.colorbar(cs2)
cbar.set_label('PST (°C)',fontsize=12) # You may edit the description of color bar 
plt.xticks(np.arange(0,6375,1274),list_long,fontsize=12)
plt.yticks(np.arange(0,4800,959),list_lat,fontsize=12)
plt.xlabel('Longitude (°E)', fontsize=12)
plt.ylabel('Latitude (°N)', fontsize=12)

x      = np.linspace(0, 6375, 22)
y      = np.linspace(0, 4800, 17)
X, Y  = np.meshgrid(x,y)

Q = plt.quiver(X, Y, wind_u_out, wind_v_out, pivot='middle', scale=100, color='black')
qk = plt.quiverkey(Q, 0.85, 0.9, 5, r'$5 \frac{m}{s}$', labelpos='E',coordinates='figure')

plt.savefig('/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/3. Results - Baseline, PFM, and slopes/3.1 Baseline/Wind_10m_2PM_wholeHK.png',dpi=1000) # Change to your directory and graphs output path

