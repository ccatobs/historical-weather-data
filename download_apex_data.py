import matplotlib.pyplot as plt
import datetime
import requests
import urllib
import time
from bs4 import BeautifulSoup
import os
import pandas as pd
import zipfile
import seaborn as sns
import os


url="http://www.submm.caltech.edu/submm.org/site/weather/"

var_lookup = {}
var_lookup["t1"] = "Humidity"
var_lookup["t2"] = "Temperature"
var_lookup["t3"] = "DewPoint"
#var_lookup["t4"] = "Humidity"
var_lookup["t5"] = "RadiometerData"
var_lookup["goog2"] = "WindSpeed"
#var_lookup["s1"] = "AverageWindSpeed"

var_values = {}


import re
def parse_weather_data_from_apex_webpage(soup):
    data = soup.find_all("script")
    var_tables = []
    table_all = None    
    for text in data:
        if text.string is None:
            continue
        for line in text.string.split("\n"):
            if "var" in str(line):
                p = re.compile('var (.*?) = (\[\[.*?);')
                m = p.match(line)
                if m is not None:
                    var, values = m.groups()
                    if var in var_lookup:
                        var_name = var_lookup[var]
                        var_values[var_name] = values.replace("[[","").replace("]]","").replace("\\","").split("],[")
                        table = pd.DataFrame(var_values[var_name])[0].str.split(",", expand=True).rename(columns={0:'time', 1:var_name})
                        table["time"] = pd.to_datetime(table["time"],format="\"%m/%d/%Y %H:%M\"")
                        table[var_name] = pd.to_numeric(table[var_name],errors='coerce')
                        table.set_index("time",inplace=True)
                        if table_all is None:
                            table_all = table
                        else:
                            table_all  = table_all.join(table[var_name])
                        var_tables.append(table)
            #
    if table_all is None:
        return
    else:
        return table_all.groupby(["time"]).mean() 

#
def send_table_to_database(table,table_name="APEX_weather_data"):
    #host="http://localhost"
    #port=8068
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
    
    tags=[]
    skip_columns = ["date","time",None,time_column]
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
#table = parse_weather_data_from_apex_webpage(soup)


from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2013, 7, 4)
end_date = date(2019, 8, 1)
#
start_date = date(2019, 8, 2)
end_date = date(2022, 1, 13)
#start_date = date(2006, 11, 22)
#end_date = date(2006, 11, 23)
tables = []
for days, single_date in enumerate(daterange(start_date, end_date)):
    url="http://www.apex-telescope.org/weather/Historical_weather/index.htm?utdate={0}&Submit=Send".format(single_date.strftime("%d-%b-%Y"))
    print("{0}/{1} {2}".format(days,(end_date-start_date).days,url))
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = parse_weather_data_from_apex_webpage(soup)
    if table is not None:
        send_table_to_database(table,table_name="APEX_weather_data")
    else:
        print("no data found")
    time.sleep(2)
    #tables.append()
#table_all = pd.concat(tables)
#table_all.drop_duplicates(inplace=True)
