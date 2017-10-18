#! /usr/bin/python3
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Author:   Fabien Marteau <fabien.marteau@armadeus.com>
# Created:  12/10/2017
#-----------------------------------------------------------------------------
#  Copyright (2017)  Armadeus Systems
#-----------------------------------------------------------------------------
""" plotsql
"""

import matplotlib.pyplot as plt
from bokeh.plotting import figure
from bokeh.embed import components
import datetime
import sqlite3
import numpy as np
import sys


print(sys.argv)
if len(sys.argv) == 2:
    fdbpathname = sys.argv[1]
else:
    fdbpathname = 'housepower.db'


conn = sqlite3.connect(fdbpathname)
c = conn.cursor()
c.execute("select recordtime, rmsvalue from rms where recordtype='house';")
all_house_measurement = sorted(c.fetchall(), key=lambda x: x[0])

y = [value[1] for value in all_house_measurement]
x = [datetime.datetime.fromtimestamp(value[0]) for value in all_house_measurement]

plt.plot_date(x, y, fmt="-")
#        , tz='Europe/Paris')
plt.gcf().autofmt_xdate()
plt.show()
