# Combining-congestion-and-emission-data
Framework written in Python to collect and match open-source air quality and traffic congestion data. Together with comments in the code, this README should be sufficient to use and edit the code. 

-   The setup consists of two parts; the main part can be find under 'Data_collector.py' and the second part is called 'Data_matcher.py'. 
-   The framework collects open-source air-quality data from the World Air Quality Index (WAQI) and traffic congestion data from TOMTOM. 
-   It is created in such a way that the ONLY inputs into the framework are the geographical coordinates of the area you want the data collected of. 
-   Therefore is is necessary the check beforehand if the data is available within you geographical boundaries. 


-   'Data_collector.py' gathers emission and congestion data simultaneously through two different API endpoints. 
-   These endpoints require a personal API token. The tokens can be acquired through the following links: https://aqicn.org/data-platform/token/ and https://developer.tomtom.com/traffic-api/documentation/product-information/introduction 
-   These personal API tokens need to be inserted in the code. 
-   Data collection will be initialized by running 'Data_collector.py'. Data is collected every half hour. 
-   It is recommended to run in on a remote machine, since code has to run for longer periods of time. 

-   If sufficient data is collected, it has to be cleansed and match by using 'Data_matcher.py'
-   Data collected by 'Data_collector.py' has to be imported into this code. 
-   Output of 'Data_matcher.py' is the matched data based on timestamp and geographical location.


Remarks:
- 'Data_collector.py' will stop if one API endpoints generates an error. Code could be improved by adding an automatic restart without losing previous results. 
