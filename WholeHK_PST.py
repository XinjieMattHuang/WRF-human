# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Script_name: Step4_plottingPST_wholeHK(10m).py
@Created_date: Jul 3 2022
@Author:       Chang Man Hei Jeffrey - HKU Urban Climate and Air Pollution Laboratory
@Version:      1.0

@Plotting area: Whole Hong Kong
@Grid resolution: 10m x 10m
@Domain size: 4800 x 6375

Lines to edit:
1. Line 31  -   # Change to calculated PST result nc file
2. Line 47  -   # Change to your directory for LUM_HKshape.tif
3. Line 92  -   # Change to your directory and graphs output path

"""

import os,glob
import netCDF4 as nc
from netCDF4 import Dataset as NetCDFFile 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage.transform import rescale, resize, downscale_local_mean
# import cartopy.crs as ccrs
from PIL import Image

print('Reading your PST nc file ...')
nc_path = 'F:/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/WRF-HEATS codes/output/Results_10m_2PM_deltaPFM.nc' # Change to calculated PST result nc file
loadnc = nc.Dataset(nc_path,'r')

boundaryLatLong = [22.56172,114.45236,22.14208,113.81551] #North,East,South,West (Lat-Long)

def convert_coordinate(x,y):
    dLat = (boundaryLatLong[2]-boundaryLatLong[0])/480
    dLong = (boundaryLatLong[1]-boundaryLatLong[3])/638
    inputLat = (y - boundaryLatLong[2])/dLat + 480
    inputLong = (x - boundaryLatLong[3])/dLong   
    return (np.array([int(inputLat),int(inputLong)]))

pst_10m = np.array(loadnc.variables['S_deltaPFM'][:,:])
pst_10m_out = pd.DataFrame(pst_10m)  # Select domain extent fitting SLOPE data, you have to identify the extent first

print('Reading your land-use shape file ...')
im = Image.open('F:/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/3. Results - Baseline, PFM, and slopes/plotting codes/LUM_HKshape.tif') # Change to your directory for LUM_HKshape.tif
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
    #print(discret_Lat)
    discret_Lat = discret_Lat - delta_boundaryLat*960
    print(discret_Lat)
    list_lat.append(format(discret_Lat,'.2f'))

for long in range(0,6375,1275):
    discret_Long = discret_Long + delta_boundaryLong*1275
    list_long.append(format(discret_Long,'.2f'))
    
print(list_lat)
print(list_long)
print(np.arange(0,6375,1274))
print(np.arange(0,4800,959))

print('Plotting your graph ...')
fig,ax = plt.subplots(figsize=(10,6))
cs =  plt.imshow(imarray_10m_out, cmap='Greys', aspect='auto',origin='lower', clim=(0,1), alpha=0.5) # You can adjust the range of color bar with clim
cs2 =  plt.imshow(mask_LUM_land , cmap='jet', aspect='auto',origin='lower', interpolation='nearest')

cbar = plt.colorbar(cs2)
cbar.set_label('△S (W/m$^{2}$)',fontsize=12) # You may edit the description of color bar 
plt.xticks(np.arange(0,6375,1274),list_long,fontsize=12)
plt.yticks(np.arange(0,4800,959),list_lat,fontsize=12)
plt.xlabel('Longitude (°E)', fontsize=12)
plt.ylabel('Latitude (°N)', fontsize=12)

plt.savefig('F:/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/3. Results - Baseline, PFM, and slopes/3.2 PFM/PST_10m_2PM_wholeHK.png',dpi=2000) # Change to your directory and graphs output path

print('Completed !')