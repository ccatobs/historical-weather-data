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
