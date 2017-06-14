from spyre import server

import pandas as pd
#use for python 2
from urllib2 import urlopen
#use for python 3
#from urllib.request import urlopen
import json

#app classs that inherrits server.app
class dataApp(server.App):
    title = "data App"
    #the inputs are a list of dictionaries
    #the dictionaries define the attributes for each input
    inputs = [{ "type" : "text",
                   "key" : "words",
                   "label" : "words",
                   "value" : "testing 123"}]

    #list of outputs dictionaries
    outputs = [{"type" : "html",
                    "id" : "html"}]

    #params is how the inputs talk to the outputs
    #its a dictionary keyed by whatever keys we made in the inputs dict
    def getHTML(self, params):
        words=params["words"]
        #because its html we can also add html tags
        return "these are the words we made: <b>%s</b>"%words

#instence of the app
app = dataApp()
app.launch()