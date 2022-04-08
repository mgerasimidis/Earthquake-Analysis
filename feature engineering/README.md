# Data Engineering
Here I will explain the main steps I followed in order to transform the data and use them for the exploratory data analysis.

### Data
* Dataset: https://www.kaggle.com/astefopoulos/earthquakes-in-greece-19012018

### Main transformations:
* Created a dataframe from the initial one, using only earthquakes of 5 Richter and more

* Used Nominatim from geopy library in order to grab the district of the center of each earthquake, using latitude and longitude

* Classification of earthquakes, depending on their magnitude (minor, light, ... , great)