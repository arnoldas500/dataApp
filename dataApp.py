
# !! *MUST* import spyre first to avoid breaking the plots!!
from spyre import server

import os, re
import xarray as xr
import rasppy as rasp
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (15, 7)
import matplotlib.pyplot as plt

nc_regex = re.compile(".*\.nc")
nc_files = [ f for f in os.listdir() if nc_regex.match(f) ]
sites = [ re.sub(r"_lidar\.nc|_mwr\.nc", "", site) for site in nc_files ]
sites = list(set(sites))
print(sites)


#app classs that inherrits server.app
class dataApp(server.App):
    def __init__(self):
        pass

    title = "xCITE Data Laboratory"

    controls = [{
        "control_type": "hidden",
        "label": "get historical stock prices",
        "control_id": "update_map"
    },
        {
            "type": "hidden",
            "id": "update_data"
        }
    ]

    # list of outputs dictionaries
    outputs = [{
        "output_type": "html",
        "output_id": "html_id",
        "control_id": "update_map",
        "on_page_load": True
    },
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data"
        }
    ]


    def getCustomJS(self):
        file1 = open("sMap.js", "r").read()
        file2 = open("jquery-3.2.0.js", "r").read()
        file3 = open("jquery-ui.js", "r").read()
        file4 = open("layer-opacity.js", "r").read()
        file5 = open("layers.js", "r").read()
        file6 = open("update.js", "r").read()
        file7 = open("ol.js","r").read()
        plot2 = """
        			function plot(){
						var spinning_wheel = $("<img />").attr('src', "/spinning_wheel");
						$("#plot").html(spinning_wheel);

						var params = updateSharedParameters();
						params = params+"output_id=plot&";
						
						var plot = $("<img />").attr('src', "plot?"+params).on('load', function(){
							$("#plot").html("");
							$("#plot").append(plot)
						});
					}
        """
        js = """
        $(document).ajaxSuccess(function(event,xhr,options){
        spyderRun()
        });
        //$('body').on('DOMNodeInserted', spyderRun());
        """
        list = '\n'.join([file7,file2,file3,file1,file4,file5,plot2,js])
        return list

    def getCustomCSS(self):
        file = open("style.css", "r").read()
        file2 = open("ol.css", "r").read()
        css1 = """
        body {
           /* background: radial-gradient(circle, red,black, black); */ 
           /* background: linear-gradient(to right, red,orange,yellow,green,blue,indigo,violet); */
           /* background: linear-gradient(to bottom, gray, blue); */
           background: url(spinning_wheel);
        }
        h1 {
           text-transform: none !important;
           font-style: italic !important;
        }
        #html_id {
           margin-top: -17.5px;
           margin-left: 15px;
        }
        #state {
           visibility: hidden !important;
        }
        """
        return '\n'.join([file, file2, css1])

    # params is how the inputs talk to the outputs
    # its a dictionary keyed by whatever keys we made in the inputs dict
    def getHTML(self, params):
        # because its html we can also add html tags
        file = open("deems/bootstrap.html", "r")
        data = file.read()

        #words=params["words"]
        #because its html we can also add html tags
        #return "these are the words we made: <b>%s</b> "%data
        return "%s"%data

    def getData(self, params):
        date_str = '20170225'
        # site_str = params['site']
        site_str = params['state2']
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
            if ds in ['vwind']:
                lidar[params['dataset']].plot(x='Time', y='Range', center=0, robust=True)
            else:
                lidar[params['dataset']].plot(x='Time', y='Range', center=False, robust=True, cmap='jet')
        elif ds in mwr_vars:
            mwr[params['dataset']].plot(x='Time', y='Range', robust=True, cmap='jet')
        elif ds == 'barbs':
            barb_bins = .25
            lidar['Windspeed'].rasp.plot_barbs(x='Time', y='Range', components=(b'x', b'y'), resample='1H',
                                               resampley=barb_bins)
        else:
            # need to provide some type of error
            pass
        # plot barbs if desired
        print(params)
        if 'barbs' in params['checks']:
        # if params['barbs'] == 'True':
            if ds in lidar_vars:
                barb_bins = .25
            else:
                barb_bins = .25
            lidar['Windspeed'].rasp.plot_barbs(x='Time', y='Range', components=('x', 'y'),
                                               resample='1H', resampley=barb_bins, ax=plt.gca())
        if 'cape' in params['checks']:
        # if params['cape'] == 'True':
            ax2 = plt.gca().twinx()
            mwr['cape'].plot(ax=ax2, color='#444444', lw=3)
            mwr['cape'].plot(ax=ax2, color='pink', lw=1.5)
            ax2.set_ylabel('CAPE (J/kg)')
            plt.gca().set_xlim([mwr.coords['Time'].values.min(), mwr.coords['Time'].values.max()])
        # plt.title(' '.join([params['site'], params['dataset']]))
        plt.title(' '.join([params['state2'], params['dataset']]))
        return plt.gca()

if __name__ == '__main__':
    app = dataApp()

    # states = pd.unique(app.data['state'].dropna())
    states = ['ny', 'nm']
    states.sort()
    options = [{"label": "all", "value": "all"}]
    # site_options = [ {"label": site, "value": site} for site in sites ]
    # states_opts = [{"label": x.upper(), "value": x} for x in states.tolist()]
    # options.extend(states_opts)
    # the inputs are a list of dictionaries
    # the dictionaries define the attributes for each input
    app.inputs = [{
        "input_type": 'dropdown',
        "options": options,
        "variable_name": 'state',
        "action_id": "update_map"
    },
        # {
        #     "input_type": 'dropdown',
        #     "label": 'Site',
        #     "options": site_options,
        #     "variable_name": 'state2',
        #     "action_id": "update_data2"
        # },

        {
            "type": 'dropdown',
            "label": 'Choose site',
            "options": [{'label': site, 'value': site} for site in sites],
            "key": 'state2',
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
        },
        {
            "type": 'checkboxgroup',
            "label": 'Features',
            "options": [
                {"label": "Wind Barbs", "value": 'barbs'},
                {"label": "CAPE", "value": 'cape'}
            ],
            "key": 'checks',
            "action_id": "update_data"
        }
        # ,
        # {
        #     "type": 'dropdown',
        #     "label": 'Barbs? (1 barb = 10 m/s)',
        #     "options": [
        #         {"label": "No", "value": False},
        #         {"label": "Yes", "value": True}
        #     ],
        #     "key": 'barbs',
        #     "action_id": "update_data"
        # }, {
        #     "type": 'dropdown',
        #     "label": 'Overlay CAPE?',
        #     "options": [
        #         {"label": "No", "value": False},
        #         {"label": "Yes", "value": True}
        #     ],
        #     "key": 'cape',
        #     "action_id": "update_data"
        # }
    ]

    # controls = [{
    #     "type": "hidden",
    #     "id": "update_data"
    # }]
    #
    # outputs = [{
    #     "type": "plot",
    #     "id": "plot",
    #     "control_id": "update_data"
    # }
    # ]
    # instence of the app
    app.launch(host='0.0.0.0', port=9379)

