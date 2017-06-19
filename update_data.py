"""Updating data for spyre:

- Reading yesterday's data from lidar/mwr csv files
- Writing them to netCDF files
"""

import os, re
import datetime as dt
import numpy as np
import rasppy.misc as rasp

# look in lidar and mwr folders to get list of sites
base = '/mnt/nfs/farm01/mesonet/data/'
lidar_path = base + 'lidar_raw/'
mwr_path = base + 'mwr_raw/'

#  helpful functions
def process_lidar(radial_file, scan_file):
    lidar = rasp.lidar_from_csv(radial_file, scan_file)
    lidar['Windspeed'] = lidar.rasp.estimate_wind()
    lidar.coords['Range'] = lidar.coords['Range'] / 1000 # convert to km
    # remove status==0 data
    lidar['CNR'] = lidar['CNR'].where(lidar['Status'])
    lidar['DRWS'] = lidar['DRWS'].where(lidar['Status'])
    lidar['hwind'] = np.sqrt(lidar['Windspeed'].sel(Component='x') ** 2 + lidar['Windspeed'].sel(Component='y') ** 2)
    lidar['vwind'] = lidar['Windspeed'].sel(Component='z').drop('Component')
    wspeed = lidar['Windspeed']
    xstd = wspeed.sel(Component='x').resample(period, 'Time', how='std')
    ystd = wspeed.sel(Component='y').resample(period, 'Time', how='std')
    zstd = wspeed.sel(Component='z').resample(period, 'Time', how='std')
    tke = ((xstd ** 2 + ystd ** 2 + zstd ** 2) / 2).drop('Component')
    lidar = lidar.drop(['Status', 'Error', 'Confidence'])
    lidar = lidar.resample(period, 'Time')
    lidar['tke'] = tke
    lidar_nc = '_'.join([site, 'lidar.nc'])
    lidar.to_netcdf(lidar_nc)

def process_mwr(lv2_file):
    mwr = rasp.mwr_from_csv(lv2_file, resample=period)
    mwr = mwr.sel(**{'LV2 Processor': 'Zenith'}).drop('LV2 Processor')
    mwr.coords['hpascals'] = ('Range', 1013.25 * np.exp(-mwr.coords['Range'] / 7))
    mwr['cape'] = mwr.rasp.estimate_cape()
    mwr_nc = '_'.join([site, 'mwr.nc'])
    mwr.to_netcdf(mwr_nc)

# remove all the old nc files
nc_regex = re.compile(".*\.nc")
nc_files = [ f for f in os.listdir() if nc_regex.match(f) ]
for nc in nc_files:
    os.remove(nc)

# get yesterday's date
today = dt.datetime.now()
yesterday = today - dt.timedelta(days=1)
print(yesterday)
# yesterday = dt.datetime.strptime('2017-02-25', '%Y-%m-%d')


lidar_sites = [ f.name for f in os.scandir(lidar_path) if f.is_dir() ]
mwr_sites =  [ f.name for f in os.scandir(mwr_path) if f.is_dir() ]
sites = lidar_sites + list(set(mwr_sites) - set(lidar_sites))
# get rid of all the CESTM_roof numbers
sites = [ re.sub(r"CESTM_roof.*", "CESTM_roof", site) for site in sites ]
sites = list(set(sites))
# remove f
print(list(set(sites)))
for site in sites:
    print(site)
    # get lidar files to see if data is available
    lidar_data_available = False
    mwr_data_available = False
    lidar_date = yesterday.strftime('%Y%m%d')

    # find the relevant data files
    lidar_path = base + 'lidar_raw/' # reset the lidar path
    if site in lidar_sites:
        lidar_path += site + '/'
        lidar_years = map(int, os.listdir(lidar_path))
        if yesterday.year in lidar_years:
            lidar_path += str(yesterday.year) + '/'
            lidar_months = map(int, os.listdir(lidar_path))
            if yesterday.month in lidar_months:
                lidar_path += yesterday.strftime('%m') + '/'
                lidar_files = os.listdir(lidar_path)
                scan_file = lidar_date + '_scan.xml'
                if scan_file in lidar_files:
                    lidar_data_available = True
                    scan_file = lidar_path + scan_file
                    # do this later:
                    # - see if a DBS scan mode is available
                    radial_file = lidar_path + lidar_date + '_whole_radial_wind_data.csv'
                    wind_file = lidar_path + lidar_date + '_reconstruction_wind_data.csv'

    mwr_path = base + 'mwr_raw/' # reset the mwr path
    if site in mwr_sites:
        mwr_path += site + '/'
        mwr_years = map(int, os.listdir(mwr_path))
        if yesterday.year in mwr_years:
            mwr_path += str(yesterday.year) + '/'
            mwr_months = map(int, os.listdir(mwr_path))
            if yesterday.month in mwr_months:
                mwr_path += yesterday.strftime('%m') + '/'
                mwr_files = os.listdir(mwr_path)
                mwr_date = yesterday.strftime('%Y-%m-%d')
                lv2_regex = re.compile("%s_.*_lv2.csv" % mwr_date)
                lv2_files = [ f for f in mwr_files if lv2_regex.match(f) ]
                if len(lv2_files) > 0:
                    mwr_data_available = True
                    lv2_file = mwr_path + lv2_files[0]


    # write the data to netcdf
    period = '5T'
    if lidar_data_available:
        try:
            process_lidar(radial_file, scan_file)
        except:
            print('no luck-- ' + site + ' lidar')
            
    if mwr_data_available:
        try:
            process_mwr(lv2_file)
        except:
            print('no luck-- ' + site + ' mwr')
