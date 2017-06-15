from spyre import server

import pandas as pd
from urllib2 import urlopen
import json

class StockExample(server.App):
	title = "Historical Stock Prices"

	inputs = [{		"type":'dropdown',
					"label": 'Company',
					"options" : [ {"label": "Google", "value":"GOOG"},
								  {"label": "Yahoo", "value":"YHOO"},
								  {"label": "Apple", "value":"AAPL"}],
					"key": 'ticker',
					"action_id": "update_data"}]

	controls = [{	"type" : "hidden",
					"id" : "update_data"}]

	tabs = ["Plot", "Table"]

	outputs = [{ "type" : "plot",
					"id" : "plot",
					"control_id" : "update_data",
					"tab" : "Plot"},
				{ "type" : "table",
					"id" : "table_id",
					"control_id" : "update_data",
					"tab" : "Table",
					"on_page_load" : True }]

	def getData(self, params):
		ticker = params['ticker']

		return ticker

'''
	def getPlot(self, params):
		df = self.getData(params).set_index('Date').drop(['volume'],axis=1)
		plt_obj = df.plot()
		plt_obj.set_ylabel("Price")
		plt_obj.set_title(self.company_name)
		fig = plt_obj.get_figure()
		return fig
'''
app = StockExample()
app.launch(port=9097)