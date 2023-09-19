import matplotlib.pyplot as plt
import datetime
import requests
import urllib
import time
from bs4 import BeautifulSoup
import os
import pandas as pd
import zipfile
#import seaborn as sns
import os
from astropy.time import Time

def send_table_to_database(table,table_name="radiometer_pwv",tags=[]):
    host="https://logging.batleth.ph1.uni-koeln.de"
    port=""
    #
    user = ''
    password = ''
    dbname = 'CCAT'
    send_every_nth_row = 100
    #
    if port == "":
        url = "{0}/write?db={1}".format(host,dbname)
    else:
        url = "{0}:{1}/write?db={2}".format(host,port,dbname)
    #
    time_column="time"
    #
    skip_columns = ["date","time",None,time_column,"MJD"]
    value_columns = list(set(table.columns)-set(skip_columns)-set(tags))
    influx_messages=[]
    #
    for i,(ts,row) in enumerate(table.iterrows()):
        tags = ",".join(["{0}={1}".format(tag,row.get(tag)) for tag in tags])
        values = ",".join(["{0}={1}".format(tag,row.get(tag)) for tag in value_columns])
        if tags=="":
            influx_message="{0} {1}{2:20.0f}".format(table_name, values, float(ts.strftime("%s"))*1e9)
        else:
            influx_message="{0},{1} {2}{3:18.0f}".format(table_name, tags, values, float(ts.strftime("%s"))*1e9)
        #
        influx_messages.append(influx_message)
        #
        if i%send_every_nth_row==0:
            #print "{0}/{1}".format(i,len(table))
            #print "\n".join(influx_messages)
            r = requests.post(url, data="\n".join(influx_messages))
            influx_messages=[]
            print("respons code: {0}".format(r.status_code))

# files
files = {}
files["TA-1"] = "https://zenodo.org/record/3880373/files/TA-1.dat"
#files["TA-2"] = "https://zenodo.org/record/3880373/files/TA-2.dat"
#files["TA-3"] = "https://zenodo.org/record/3880373/files/TA-3.dat"
#files["TB-1"] = "https://zenodo.org/record/3880373/files/TB-1.dat"
#files["TB-2"] = "https://zenodo.org/record/3880373/files/TB-2.dat"
#files["TB-3"] = "https://zenodo.org/record/3880373/files/TB-2.dat"
#files["WVR_UdeC"] = "https://zenodo.org/record/3880373/files/WVR_UdeC.dat"

# download files
for key,filename in files.items():
    print(filename)
    print("downloading {0}".format(key,filename))
    # read url into python onject
    response = urllib.request.urlopen(filename)
    text = response.read()
    site = [line.split(":") for line in text.decode("utf-8").split("\n")[:10] if "site:" in line][0][-1]
    # extract site
    #urllib.request.urlretrieve(files[key], "radiometer_data/{0}.dat".format(key))
    # open file in pandas table
    table = pd.read_csv(filename,delim_whitespace=True,skiprows=10,names=["MJD","pwv"])
    table["time"] = pd.to_datetime(Time(table["MJD"]+2400000.5,format="jd").to_datetime())
    table.set_index("time",inplace=True)
    table["site"] = site
    #
    send_table_to_database(table,table_name="radiometer_pwv",tags=["site"])
