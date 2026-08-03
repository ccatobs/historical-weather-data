# CCAT Historical Weather Data

An archive of weather measurements made on Cerro Chajnantor from 2006-2014
to characterize the CCAT site, cleaned and merged into a single file.

Original data source is [here](http://www.submm.caltech.edu/submm.org/site/weather/cc.html).
Downloaded 2019-11-26.

The merged dataset can be read using python and pandas:

```python
import pandas
df = pandas.read_csv("ccat_site_weather_data_2006_to_2014.csv", parse_dates=['datetime'])
```

## Event log

```
2012 October 27 15:04 UT
  Clock 1 min ahead; reset to UT.
2011 November 5 16:38 UT
  Clock 2 min ahead; reset to UT.
2010 April 4 17:05 UT
  Clock 2 min ahead; reset to UT.
2010 January 26 17:56 UT
  Replace anemometer.
2009 September 27 14:59 UT
  Anemometer broken.
2009 March 19 15:08 UT
  Clock 3 min ahead; reset to UT.
2006 May 11
  Unit 2 installed, clock set to UT.
```
