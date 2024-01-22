# -*- coding: utf-8 -*-
"""
@Script_name:  HongKong_Kowloon_PSTwith_satellite_and_LUM_and_wind(10m).py
@Created_date: Sep 19 2022
@Author:       Chang Man Hei Jeffrey - HKU Urban Climate and Air Pollution Laboratory
@Version:      1.0
@Plotting area: Kowloon and Northern HK Island
@Grid resolution: 10m x 10m
@Domain size: 700 x 800
Lines to edit: 
1. Line 37  -   # Change to your directory for PST.nc file (wrfout_10meters_horizontal_Hour103.nc)
2. Line 41  -   # Change to your directory for wrfout.nc file (wrfout_333meters_11elements.nc)
3. Line 46  -   # Change the Latitude and Longitude of the map extent (if needed)
4. Line 68  -   # Change to your directory for LUM_HKshape.tif
5. Line 137  -   # Change to your directory and graphs output path
6. Line 45  -   # If you want to plot the wind arrows WITH ANOTHER TIMESTAMP from 333m WRF file 
                  Edit "timestamp" in Line 
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
nc_path = '/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/WRF-HEATS codes/output/Results_10m_2PM_tandq.nc' # Change to calculated PST result nc file
loadnc = nc.Dataset(nc_path,'r')

print('Reading your wrfout nc file ...')
wrfout_path = '/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/WRF-HEATS codes/wrfout_333meters_11elements.nc'
loadwrfout = nc.Dataset(wrfout_path,'r')


timestamp1 = 55
timestamp2 = 79
timestamp3 = 103
timestamp4 = 127
timestamp5 = 151
boundaryLatLong = [22.340,114.210,22.270,114.136] #North,East,South,West (Lat-Long)


def convert_coordinate(x,y):
    dLat = (boundaryLatLong[2]-boundaryLatLong[0])/480
    dLong = (boundaryLatLong[1]-boundaryLatLong[3])/638
    inputLat = (y - boundaryLatLong[2])/dLat + 480
    inputLong = (x - boundaryLatLong[3])/dLong   
    return (np.array([int(inputLat),int(inputLong)]))

pst_10m = np.array(loadnc.variables['t'][:,:])
pst_10m_out = pd.DataFrame(pst_10m)  # Select domain extent fitting SLOPE data, you have to identify the extent first

print('Reading your land-use file ...')
im = Image.open('/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/3. Results - Baseline, PFM, and slopes/plotting codes/LUM_Full.tif') # Change to your directory for LUM_Full.tif
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

wind_u1 = np.array(loadwrfout.variables['U10'][timestamp1,41:63,96:120])
wind_u2 = np.array(loadwrfout.variables['U10'][timestamp2,41:63,96:120])
wind_u3 = np.array(loadwrfout.variables['U10'][timestamp3,41:63,96:120])
wind_u4 = np.array(loadwrfout.variables['U10'][timestamp4,41:63,96:120])
wind_u5 = np.array(loadwrfout.variables['U10'][timestamp5,41:63,96:120])
wind_u = (wind_u1 + wind_u2 + wind_u3 + wind_u4 + wind_u5)/5;
wind_u_out = pd.DataFrame(wind_u).iloc[1:,:]

wind_v1 = np.array(loadwrfout.variables['V10'][timestamp1,41:63,96:120])
wind_v2 = np.array(loadwrfout.variables['V10'][timestamp2,41:63,96:120])
wind_v3 = np.array(loadwrfout.variables['V10'][timestamp3,41:63,96:120])
wind_v4 = np.array(loadwrfout.variables['V10'][timestamp4,41:63,96:120])
wind_v5 = np.array(loadwrfout.variables['V10'][timestamp5,41:63,96:120])
wind_v = (wind_v1 + wind_v2 + wind_v3 + wind_v4 + wind_v5)/5;
wind_v_out = pd.DataFrame(wind_v).iloc[1:,:]

#wind_u = np.array(loadwrfout.variables['U10'][timestamp,41:63,96:120])
#wind_u_out = pd.DataFrame(wind_u).iloc[1:,:]

#wind_v = np.array(loadwrfout.variables['V10'][timestamp,41:63,96:120])
#wind_v_out = pd.DataFrame(wind_v).iloc[1:,:]


list_lat = []
list_long = []
delta_boundaryLat = (boundaryLatLong[2]-boundaryLatLong[0])/700 #Southern boundary - Northern boundary for HK
delta_boundaryLong = (boundaryLatLong[1]-boundaryLatLong[3])/800 #Eastern boundary - Western boundary for HK
discret_Lat = boundaryLatLong[2]
discret_Long = boundaryLatLong[3]

list_lat.append(format(discret_Lat,'.2f'))
list_long.append(format(discret_Long,'.2f'))

for lat in range(0,700,100): #234
    #print(discret_Lat)
    discret_Lat = discret_Lat - delta_boundaryLat*100 #234
    print(discret_Lat)
    list_lat.append(format(discret_Lat,'.2f'))

for long in range(0,800,115): #267
    discret_Long = discret_Long + delta_boundaryLong*115 #267
    list_long.append(format(discret_Long,'.2f'))
    
print(list_lat)
print(list_long)

print('Reading your satellite background file ...')
satellite = plt.imread('/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/3. Results - Baseline, PFM, and slopes/plotting codes/Satellite_KowloonHK_inverted.png') # Change to your directory for Satellite_KowloonHK_inverted.png
## PNG file "Satellite_KowloonHK_inverted.png" is available in GitHub

print('Plotting your graph ...')
fig,ax = plt.subplots(figsize=(10,8))

## Turn on cs for overlaying satellite image from PNG file as background, alpha = transparency 
## cs2 is for the masking of road layers with PST input
## cs3 is for the masking of openspace layers with PST input
## If you want both Openspace and Roads layers in the same figure, turn on both lines

cs =   plt.imshow(satellite,alpha=0.5, aspect='auto')
cs2 =  plt.imshow(mask_pst_roads.iloc[1450:2150,3200:4000] , cmap='jet', aspect='auto',origin='lower', interpolation='nearest')  # You can adjust the range of color bar with clim
cs3 =  plt.imshow(mask_pst_openspace.iloc[1450:2150,3200:4000] , cmap='jet', aspect='auto',origin='lower', interpolation='nearest')

cbar = plt.colorbar(cs3)
cbar.set_label('Q2 (g/kg)',fontsize=12) # You may edit the description of color bar 
plt.xticks(np.arange(0,800,114),list_long,fontsize=12) #266
plt.yticks(np.arange(0,700,99),list_lat,fontsize=12) #233
plt.xlabel('Longitude(°E)', fontsize=12)
plt.ylabel('Latitude (°N)', fontsize=12)

x      = np.linspace(0, 799, 24)
y      = np.linspace(0, 699, 21)
X, Y  = np.meshgrid(x,y)

Q = plt.quiver(X, Y, wind_u_out, wind_v_out, pivot='mid', scale=100, color='black')
qk = plt.quiverkey(Q, 0.85, 0.9, 5, r'$5 \frac{m}{s}$', labelpos='E',coordinates='figure')

#plt.savefig('F:/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/3. Results - Baseline, PFM, and slopes/3.1 Baseline/Windandq_333m_2PM.png',dpi=2000) # Change to your directory and graphs output path

print('Completed !')

t_2PM_roads = mask_pst_roads.iloc[1450:2150,3200:4000].values.flatten()

t_2PM_openspace = mask_pst_openspace.iloc[1450:2150,3200:4000].values.flatten()

np.savetxt('F:/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/3. Results - Baseline, PFM, and slopes/3.1 Baseline/t_2PM_roads.csv', t_2PM_roads , delimiter=',')

np.savetxt('F:/OneDrive - connect.hku.hk/Xinjie Huang/6 WRF+HEATS/Work/3. Results - Baseline, PFM, and slopes/3.1 Baseline/t_2PM_openspace.csv', t_2PM_openspace , delimiter=',')