'''
from spyre import server

class SimpleApp(server.App):
	title = "Simple App"
	inputs = [{
		"type": "text",
		"key": "words",
		"label": "write words here",
		"value": "hello world testing",
		"action_id": "simple_html_output"
	}]

	outputs = [{
		"type": "html",
		"id": "simple_html_output"
	}]

	def getHTML(self, params):
		words = params["words"]
		return "Here's what you wrote in the textbox: <b>%s</b>" % words

app = SimpleApp()
app.launch()
'''

#NEWWWWW

import os, re
import datetime as dt
#import rasppy.misc as rasp

# get yesterday's date
today = dt.datetime.now()
yesterday = today - dt.timedelta(days=1)

# look in lidar and mwr folders to get list of sites
base = '/mnt/nfs/farm01/mesonet/data/'
lidar_path = base + 'lidar_raw/'
mwr_path = base + 'mwr_raw/'
lidar_sites = os.listdir(lidar_path)
mwr_sites = os.listdir(mwr_path)
sites = lidar_sites + list(set(mwr_sites) - set(lidar_sites))

from spyre import server

import pandas as pd
import numpy as np

from bokeh.io import output_file, show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
)

from bokeh.resources import INLINE
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.sampledata import us_counties, unemployment
from bokeh import plotting
from collections import OrderedDict
try:
    from bokeh.objects import HoverTool
except ImportError:
    from bokeh.models import HoverTool


class UnemploymentApp(server.App):
    def __init__(self):
        colors = ["#F1EEF6", "#D4B9DA", "#C994C7", "#DF65B0", "#DD1C77", "#980043"]
        stuff = []
        for key in us_counties.data:
            stuff.append(us_counties.data[key])
        shapes = pd.DataFrame(stuff, index=us_counties.data.keys())
        unemp = pd.DataFrame(
            list(unemployment.data.values()),
            index=list(unemployment.data.keys()),
            columns=['rate']
        )
        unemp['idx'] = (unemp['rate'] // 2).astype('i8')
        unemp[unemp['idx'] > 5] = 5
        unemp['color'] = [colors[idx] for idx in unemp['idx'].tolist()]
        data = unemp.join(shapes)
        data['mlong'] = list(map(np.mean, data['lons']))
        data['mlats'] = list(map(np.mean, data['lats']))
        data = data[(data['mlong'] > -130) & (data['mlong'] < -65)]
        data = data[(data['mlats'] > 25) & (data['mlats'] < 50)]
        self.data = data

    title = "Profiler Data"

    controls = [{
        "control_type": "hidden",
        "label": "get historical stock prices",
        "control_id": "update_data"
    }]

    outputs = [{
        "output_type": "html",
        "output_id": "html_id",
        "control_id": "update_data",
        "on_page_load": True
    }]

    # def getHTML(self, params):
    #     # state = params['state']
    #     state='ny'
    #     # if state == 'NY':
    #     #     data = self.data
    #     # else:
    #     data = self.data[self.data['state'] == 'ny']
    #
    #     TOOLS = "pan,wheel_zoom,box_zoom,reset,hover,previewsave"
    #
    #     try:
    #         fig = plotting.patches(
    #             data['lons'], data['lats'], fill_color=data['color'], fill_alpha=0.7, tools=TOOLS,
    #             line_color="white", line_width=0.5, title=state.upper() + " Profiler Data"
    #         )
    #     except Exception:
    #         fig = plotting.figure(title=state.upper() + " Profiler Data", tools=TOOLS)
    #         fig.patches(
    #             data['lons'], data['lats'], fill_color=data['color'],
    #             fill_alpha=0.7, line_color="white", line_width=0.5
    #         )
    #
    #     hover = fig.select(dict(type=HoverTool))
    #     hover.tooltips = OrderedDict([
    #         ("index", "$index")
    #     ])
    #
    #     script, div = components(fig, CDN)
    #     html = "%s\n%s" % (script, div)
    #     return html



    def getCustomJS(self):
        file1 = open("sMap.js", "r").read()
        file2 = open("jquery-3.2.0.js", "r").read()
        file3 = open("jquery-ui.js", "r").read()
        file4 = open("layer-opacity.js", "r").read()
        file5 = open("layers.js", "r").read()
        file6 = open("update.js", "r").read()
        file7 = open("ol.js","r").read()
        js = """
        $(document).ajaxSuccess(function(event,xhr,options){
        spyderRun()
        });
        //$('body').on('DOMNodeInserted', spyderRun());
        """
        list = '\n'.join([file7,file2,file3,file1,file4,file5,js])
        return list

    def getCustomCSS(self):
        return INLINE.css_raw[0]

    def getHTML(self, params):
        file = open("deems/bootstrap.html", "r")
        data = file.read()

        #words=params["words"]
        #because its html we can also add html tags
        #return "these are the words we made: <b>%s</b> "%data
        return "%s"%data

if __name__ == '__main__':
    app = UnemploymentApp()

    states = pd.unique(app.data['state'].dropna())
    states.sort()
    options = [{"label": "all", "value": "all"}]
    site_options = [ {"label": site, "value": site} for site in sites ]
    states_opts = [{"label": x.upper(), "value": x} for x in states.tolist()]
    options.extend(states_opts)
    app.inputs = [{
        "input_type": 'dropdown',
        "label": 'Site',
        "options": options,
        "variable_name": 'state',
        "action_id": "update_data"
    },
        {
            "input_type": 'dropdown',
            "label": 'Site',
            "options": site_options,
            "variable_name": 'state2',
            "action_id": "update_data2"
        }
    ]
    app.launch(port=9097)

