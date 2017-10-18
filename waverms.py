#! /usr/bin/python3
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Author:   Fabien Marteau <fabien.marteau@armadeus.com>
# Created:  03/10/2017
#-----------------------------------------------------------------------------
#  Copyright (2017)  Armadeus Systems
#-----------------------------------------------------------------------------
""" waverms
"""

import numpy as np
import sqlite3
import audioop
import getopt
import time
import wave
import sys
import os

class waverms(object):
    """
    """

def usage():
    print("Usage:")
    print("$ python3 waverms [options]")
    print("-h, --help       print this help message")
    print("-n, --name       give prefix name of records(default rec)")
    print("-d, --dir        give directory to record wavefiles (default hdata)")
    print("-c, --csvname    give the csv name file (default rms.csv)")
    print("-s, --sqlitefile give sqlite3 filename") 


if __name__ == "__main__":
    print("waverms class test\n")

    if sys.version_info[0] < 3:
        raise Exception("Must be using Python 3")

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:t:d:s:",
                                    ["help", "name=",
                                     "time=", "dir=",
                                     "sqlitefile="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)


    wavename = "rec"
    hdata = "hdata"
    csvname = "rms.csv"
    sqlitefile = "housepower.db"
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-n", "--name"):
            wavename = arg
        elif opt in ("-t", "--time"):
            wavetime = int(arg)
        elif opt in ("-d", "--dir"):
            hdata = arg
        elif opt in ("-s", "--sqlitefile"):
            sqlitefile = arg

    while True:
        wavelist = [value for value in os.listdir(hdata) if wavename == value.split("-")[0]]
        if wavelist == []:
            print("No new file, waiting")
            time.sleep(30)
            continue

        fsql = sqlite3.connect(sqlitefile)
        cursor = fsql.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS rms
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                recordtype VARCHAR(20), rmsvalue INTEGER,
                recordtime INTEGER);""")

        if not os.path.exists(csvname):
            fcsv = open(csvname, "w")
            fcsv.write("epoch_time, rms\n")
        else:
            fcsv = open(csvname, "a+")

        for filename in wavelist:
            pathfilename = "/".join([hdata,filename])
            with wave.open(pathfilename, "r") as spf:
                signal = spf.readframes(-1)
                signal = np.fromstring(signal, 'Int16')
                rms = audioop.rms(signal, 2)
                epoch_time = filename.split("-")[1].split(".")[0]
            fcsv.write("{}, {}\n".format(epoch_time, rms))
            cursor.execute("INSERT INTO rms VALUES (NULL, 'house', {}, {});"
                           .format(rms, epoch_time)) 
            print("{} -> {}".format(epoch_time, rms))
            os.remove(pathfilename)
        fsql.commit()
        fsql.close()
        fcsv.close()
