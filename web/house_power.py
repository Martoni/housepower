from flask import Flask
from flask import render_template
import matplotlib.pyplot as plt
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN 
from bokeh.util.string import encode_utf8

import datetime
import sqlite3
import numpy as np
import sys

app = Flask(__name__)

class HousePower(object):
    """ House power class """

    def __init__(self, sqlitefilename):
        self.sqfln = sqlitefilename

HPR = HousePower('../housepower.db')

@app.route('/')
def hello():
    conn = sqlite3.connect(HPR.sqfln)
    c = conn.cursor()
    datemax = datetime.datetime.now()
    datemin = datemax - datetime.timedelta(days=1)
    query = ("select recordtime, rmsvalue " +
             "from rms " +
             "where recordtype='house' and " +
             "recordtime > {} and recordtime < {};"
             .format(datemin.timestamp(), datemax.timestamp()))
    c.execute(query)
    all_house_measurement = sorted(c.fetchall(), key=lambda x: x[0])
    
    y = [value[1] for value in all_house_measurement]
    x = [datetime.datetime.fromtimestamp(value[0]) for value in all_house_measurement]
    TOOLS="pan,wheel_zoom,box_zoom,reset,save"
    plot = figure(tools=TOOLS,
                  title=u'Consommation Électrique',
                  x_axis_label='date', x_axis_type='datetime',
                  y_axis_label='RMS current', 
                  plot_width=1000, plot_height=500)

    plot.line(x=x, y=y)


    bk_script, bk_div = components(plot, CDN)
    return render_template('graph.html',
            bk_script=bk_script, bk_div=bk_div)

if __name__ == '__main__':
    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")

    if len(sys.argv) == 2:
        HPR.sqfln = sys.argv[1]

    print("DB used : {}".format(HPR.sqfln))
    app.debug = True
    app.run(host='0.0.0.0')

