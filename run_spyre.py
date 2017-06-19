"""A simple spyre test script"""

# !! *MUST* import spyre first to avoid breaking the plots!!
from spyre import server

import os, re
import xarray as xr
import rasppy as rasp
import matplotlib as mpl
# mpl.use('Agg')
mpl.rcParams['figure.figsize'] = (15, 7)
import matplotlib.pyplot as plt

nc_regex = re.compile(".*\.nc")
nc_files = [ f for f in os.listdir() if nc_regex.match(f) ]
sites = [ re.sub(r"_lidar\.nc|_mwr\.nc", "", site) for site in nc_files ]
sites = list(set(sites))
print(sites)



class SimpleApp(server.App):
    title = "xCITE Data Laboratory"
    inputs = [{
	"type": 'dropdown',
	"label": 'Choose site',
	"options": [ {'label': site, 'value': site} for site in sites ],
	"key": 'site',
	"action_id": "update_data"
    }, {
	"type": 'dropdown',
	"label": 'Choose dataset',
	"options": [
	    {"label": "CNR", "value": "CNR"},
	    {"label": "DRWS", "value": "DRWS"},
	    {"label": "Horizontal Wind Speed", "value": "hwind"},
            {"label": "Wind Barbs", "value": "barbs"},
            {"label": "Vertical Wind Speed", "value": "vwind"},
            {"label": "Temperature", "value": "Temperature"},
            {"label": "Relative Humidity", "value": "Relative Humidity"},
            {"label": "Vapor Density", "value": "Vapor Density"},
            {"label": "Liquid", "value": "Liquid"},
            {"label": "Turbulence Kinetic Energy", "value": "tke"}
	],
	"key": 'dataset', 
	"action_id": "update_data"
    }, {
	"type": 'dropdown',
	"label": 'Barbs? (1 barb = 10 m/s)',
	"options": [
	    {"label": "No", "value": False},
	    {"label": "Yes", "value": True}
	],
	"key": 'barbs', 
	"action_id": "update_data"
    }, {
	"type": 'dropdown',
	"label": 'Overlay CAPE?',
	"options": [
	    {"label": "No", "value": False},
	    {"label": "Yes", "value": True}
	],
	"key": 'cape',
	"action_id": "update_data"
    }]

    controls = [{
	"type": "hidden",
	"id": "update_data"
    }]

    outputs = [{
	"type": "plot",
	"id": "plot",
	"control_id": "update_data"
    }]


#got everything below
    def getData (self, params):
        date_str = '20170225'
        site_str = params['site']
        lidar_file = '_'.join([site_str, 'lidar.nc'])
        mwr_file = '_'.join([site_str, 'mwr.nc'])
        files = os.listdir('.')
        if lidar_file in files:
            lidar = xr.open_dataset(lidar_file)
        else:
            lidar = None
        if mwr_file in files:
            mwr = xr.open_dataset(mwr_file)
        else:
            mwr = None
        return [lidar, mwr]

    def getPlot(self, params):
        # just a plain heatmap for now
        [lidar, mwr] = self.getData(params)
        if lidar is not None:
            lidar_vars = list(lidar.data_vars)
        else:
            lidar_vars = []
        if mwr is not None:
            mwr_vars = list(mwr.data_vars)
        else:
            mwr_vars = []
        ds = params['dataset']
        if ds in lidar_vars:
            if params['dataset'] in ['vwind']:
                lidar[params['dataset']].plot(x='Time', y='Range', center=0, robust=True)
            else:
                lidar[params['dataset']].plot(x='Time', y='Range', center=False, robust=True, cmap='jet')
        elif ds in mwr_vars:
            mwr[params['dataset']].plot(x='Time', y='Range', robust=True, cmap='jet')
        elif ds == 'barbs':
            barb_bins = .25
            lidar['Windspeed'].rasp.plot_barbs(x='Time', y='Range', components=(b'x', b'y'), resample='1H', resampley=barb_bins)
        else:
            # need to provide some type of error
            pass
        # plot barbs if desired
        if params['barbs'] == 'True':
            if ds in lidar_vars:
                barb_bins = .25
            else:
                barb_bins = .25
            lidar['Windspeed'].rasp.plot_barbs(x='Time', y='Range', components=('x', 'y'),
                                               resample='1H', resampley=barb_bins, ax=plt.gca())
        if params['cape'] == 'True':
            ax2 = plt.gca().twinx()
            mwr['cape'].plot(ax=ax2, color='#444444', lw=3)
            mwr['cape'].plot(ax=ax2, color='pink', lw=1.5)
            ax2.set_ylabel('CAPE (J/kg)')
            plt.gca().set_xlim([mwr.coords['Time'].values.min(),mwr.coords['Time'].values.max()])
        plt.title(' '.join([params['site'], params['dataset']]))
        return plt.gcf()
        # return plot

app = SimpleApp()
app.launch()
