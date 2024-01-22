# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 20:36:31 2022

@author: xh2892
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Script_name: Step4_plottingPSTdata_with_satellite_and_LUM(10m).py
@Created_date: Jul 3 2022
@Author:       Chang Man Hei Jeffrey - HKU Urban Climate and Air Pollution Laboratory
@Version:      1.0
@Plotting area: Kowloon and Northern HK Island
@Grid resolution: 10m x 10m
@Domain size: 4800 x 6375
Lines to edit:
1. Line 32  -   # Change to calculated PST result nc file
2. Line 48  -   # Change to your directory for LUM_Full.tif
3. Line 90  -   # Change to your directory for Satellite_KowloonHK_inverted.png (background satellite photo)
4. Line 113 -   # Change to your directory and graphs output path
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
#nc_path = 'F:/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/WRF-HEATS codes/output/Results_10m_2PM_deltaslope.nc' # Change to calculated PST result nc file
nc_path = 'C:/Users/Matt/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/WRF-HEATS codes/output/Results_10m_2PM_deltaslope.nc'
loadnc = nc.Dataset(nc_path,'r')

boundaryLatLong = [22.340,114.210,22.270,114.136] #North,East,South,West (Lat-Long)

def convert_coordinate(x,y):
    dLat = (boundaryLatLong[2]-boundaryLatLong[0])/480
    dLong = (boundaryLatLong[1]-boundaryLatLong[3])/638
    inputLat = (y - boundaryLatLong[2])/dLat + 480
    inputLong = (x - boundaryLatLong[3])/dLong   
    return (np.array([int(inputLat),int(inputLong)]))

pst_10m = np.array(loadnc.variables['PST_deltaslope'][:,:])
pst_10m[pst_10m < 0.5] = 'nan'
pst_10m_out = pd.DataFrame(pst_10m)  # Select domain extent fitting SLOPE data, you have to identify the extent first

print('Reading your land-use file ...')
im = Image.open('C:/Users/Matt/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/3. Results - Baseline, PFM, and slopes/plotting codes/LUM_Full.tif') # Change to your directory for LUM_Full.tif
imarray_10m = pd.DataFrame(np.array(im))
imarray_10m_out = pd.DataFrame(imarray_10m).iloc[::-1,:]


mask_reset = imarray_10m_out==32  ## 32 for openspace (LUM manual)
mask_reset = mask_reset.reset_index(drop=True)

mask_reset2 = imarray_10m_out==41  ## 41 for raods (LUM manual)
mask_reset2 = mask_reset2.reset_index(drop=True)

mask_LUM_openspace = pst_10m_out[mask_reset]
mask_LUM_roads = pst_10m_out[mask_reset2]

mask_pst_openspace = mask_LUM_openspace.iloc[1:,:]
mask_pst_roads = mask_LUM_roads.iloc[1:,:]


list_lat = []
list_long = []
delta_boundaryLat = (boundaryLatLong[2]-boundaryLatLong[0])/700 #Southern boundary - Northern boundary for HK
delta_boundaryLong = (boundaryLatLong[1]-boundaryLatLong[3])/800 #Eastern boundary - Western boundary for HK
discret_Lat = boundaryLatLong[2]
discret_Long = boundaryLatLong[3]

list_lat.append(format(discret_Lat,'.2f'))
list_long.append(format(discret_Long,'.2f'))

for lat in range(0,700,100):
    #print(discret_Lat)
    discret_Lat = discret_Lat - delta_boundaryLat*100
    print(discret_Lat)
    list_lat.append(format(discret_Lat,'.2f'))

for long in range(0,800,115):
    discret_Long = discret_Long + delta_boundaryLong*115
    list_long.append(format(discret_Long,'.2f'))
    
print(list_lat)
print(list_long)

print('Reading your satellite background file ...')
satellite = plt.imread('C:/Users/Matt/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/3. Results - Baseline, PFM, and slopes/plotting codes/Satellite_KowloonHK_inverted_BnW.png') # Change to your directory for Satellite_KowloonHK_inverted.png
## PNG file "Satellite_KowloonHK_inverted.png" is available in GitHub

print('Plotting your graph ...')
fig,ax = plt.subplots(figsize=(10,8))

## Turn on cs for overlaying satellite image from PNG file as background, alpha = transparency 
## cs2 is for the masking of road layers with PST input
## cs3 is for the masking of openspace layers with PST input
## If you want both Openspace and Roads layers in the same figure, turn on both lines

cs = plt.imshow(satellite,alpha=0.5, aspect='auto')
cs2 =  plt.imshow(mask_pst_roads.iloc[1450:2150,3200:4000] , cmap='YlOrRd', aspect='auto',origin='lower', clim=(0.5,22.6),interpolation='nearest')  # You can adjust the range of color bar with clim
cs3 =  plt.imshow(mask_pst_openspace.iloc[1450:2150,3200:4000] , cmap='YlOrRd', aspect='auto',origin='lower', clim=(0.5,22.6),interpolation='nearest') #YlOrRd

ticks = np.linspace(0.5, 22.5, 12, endpoint=True)
cbar = plt.colorbar(ticks=ticks)

#cbar = plt.colorbar(cs3)
#cbar.ax.locator_params(nbins=12)
cbar.ax.tick_params(labelsize=15)
cbar.set_label('△PST_slope (°C)',fontsize=20) # You may edit the description of color bar 
plt.xticks(np.arange(0,800,114),list_long,fontsize=15)
plt.yticks(np.arange(0,700,99),list_lat,fontsize=15)
plt.xlabel('Longitude (°E)', fontsize=20)
plt.ylabel('Latitude (°N)', fontsize=20)
#plt.show()

plt.savefig('C:/Users/Matt/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/3. Results - Baseline, PFM, and slopes/3.3 Slope/PST_10m_2PM_KowHK_BnW_YlOrRd_0.5legend.png',dpi=2000) # Change to your directory and graphs output path

print('Completed !')