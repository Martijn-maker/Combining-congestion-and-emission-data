import matplotlib.pyplot as plt
import pandas as pd
import json
import requests
import numpy as np 
from datetime import datetime, timedelta
import time
import numpy as np
import seaborn as sns

### insert the .csv files which where created with the Data_collecor_total.py

df_congestion = pd.read_csv(r'Your_File_name.csv')
df_emission = pd.read_csv(r'Your_File_name2')

###


df_emission= df_emission.drop_duplicates(subset=['time','uid'], keep="first")
df_congestion['time'] = pd.to_datetime(df_congestion['time'])
df_emission['time'] = pd.to_datetime(df_emission['time'])
df_congestion['time'] = df_congestion['time'] + timedelta(hours=5,minutes=30)
df_emission.index = pd.to_datetime(df_emission.index)
df_total = pd.merge_asof(df_emission.sort_values('time'), df_congestion, on="time", by= 'uid', direction= 'nearest')


### Name excel with all total data 

df_total.to_excel('matching_2_10115.xls')

###

