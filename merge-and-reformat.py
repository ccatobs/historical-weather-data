#!/usr/bin/env python3

import datetime
import os
import os.path

import numpy as np
import pandas as pd

datadir = "./data/"
input_column_names = ["unit","date","rawtime","wind_speed_avg_mps","wind_direction_avg_deg",
    "wind_direction_stddev_deg","wind_speed_peak_mps","temperature_C",
    "relative_humidity","pressure_mbar","battery_V","zero"]
output_column_names = ["temperature_C","pressure_mbar","relative_humidity",
    "wind_speed_avg_mps","wind_speed_peak_mps",
    "wind_direction_avg_deg","wind_direction_stddev_deg"]

# read and merge
dfs = []
for name in sorted(os.listdir(datadir)):
    filename = os.path.join(datadir, name)
    print(f"reading {filename}")
    df = pd.read_csv(filename, names=input_column_names, index_col=False, comment='#')
    dfs.append(df)
df = pd.concat(dfs)
df.drop_duplicates(inplace=True)
del(dfs)

# create datetime index
df["datetime"] = pd.to_datetime(df['date'] +' '+ df['rawtime'], format="%y/%m/%d %H:%M:%S", utc=True)
df.set_index("datetime", inplace=True)

# sanity checks
assert df['unit'].min() == 2
assert df['unit'].max() == 2
for column in output_column_names:
    assert df[column].dtype in [np.int64, np.float64]

# write output file
filename = "ccat_site_weather_data_2006_to_2014.csv"
print(f"writing {filename}")
df.to_csv(filename, columns=output_column_names)

