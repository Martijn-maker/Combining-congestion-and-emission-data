import matplotlib.pyplot as plt
import pandas as pd
import json
import requests
import numpy as np 
import datetime
import time
import numpy as np
import schedule

### Define the .csv files you want your data written to ###
congestion_file = 'congestion_Data.csv'
emission_file   = 'emission_Data.csv'



#New Delhi city area coordinates 
upper_bound = '28.973265,76.649430'
lower_bound = '28.434276,77.768612'


### THESE COORDINATES INCLUDE 3 EMISSION MEASUREMENT STATIONS IN AMSTERDAM 
#upper_bound = '52.36385558300145,4.838298389322255'
#lower_bound = '52.25113880526266,4.998274400224975'


def choose_city_by_coordinates(upper_bound, lower_bound):
    url = 'https://api.waqi.info/map/bounds?token='Your_persoonal_token'&latlng='
    response_city_stations = requests.get(url+str(upper_bound)+','+str(lower_bound))
    city_stations = json.loads(response_city_stations.content)
    city_stations = city_stations['data']
    df_city_stations = pd.DataFrame(city_stations)
    df_city_stations = pd.concat([df_city_stations, df_city_stations["station"].apply(pd.Series)], axis=1)
    df_city_stations = df_city_stations.drop(columns='station')
    return(df_city_stations)


def get_geo_coordinates_per_station():
    url_geo_part1 = 'https://api.waqi.info/feed/@'
    url_geo_part2 = '/?token='Your_personal_token'
    city_stations2 = choose_city_by_coordinates(upper_bound, lower_bound)
    df = pd.DataFrame([])
    df2 = pd.DataFrame([])
    for i in city_stations2['uid']:
        url_geo_total = url_geo_part1 + str(i) + url_geo_part2
        response4 = requests.get(url_geo_total)
        data = json.loads(response4.content)
        data1 = data['data']['city']['geo']
        data2 = data['data']['idx']
        row_data =pd.DataFrame([data1])
        row_data2 =pd.DataFrame([data2])
        #row_data = pd.DataFrame([data])
        row_data.rename(columns = {0:'lat', 1:'lon'}, inplace = True)
        #row_data2.rename(columns = {0:'uid'}, inplace = True)
        df = pd.concat([df,row_data]) 
        df2 = pd.concat([df2,row_data2])
        df['uid'] = df2
    return(df)


def get_congestion_data_per_station(coord_lat, coord_lon,coord_uid):
    apiKey = '9dJa27yI9BdrbvBh5kW4Y5D5ey33MZtG'
    response = requests.get('https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json?point='+coord_lat+'%2C'+coord_lon+'&unit=KMPH&openLr=false&key='+apiKey+'')
    request_text = response.text
    tomtom = json.loads(request_text)
    df_t = pd.DataFrame.from_dict(tomtom['flowSegmentData'])
    df_t = df_t.drop(['coordinates','@version'], axis=1)
    e = datetime.datetime.now()
    e = e.strftime("%Y-%m-%d %H:%M:%S")
    df_t['time'] = e
    
    #df_t = df_t.set_index('time')
    
    df_t['lat'] = coord_lat 
    df_t['lon'] = coord_lon
    df_t['uid'] = int(coord_uid)
    #df_t = df_t.to_dict('split')
    return(df_t)

def get_total_congestion_data():
    coord = get_geo_coordinates_per_station()
    coord_lon = coord['lat']
    coord_lat = coord['lon']
    coord_uid = coord['uid']
    df = pd.DataFrame([])
    city_stations = choose_city_by_coordinates(upper_bound, lower_bound)
    for i,j,k in zip(coord['lat'], coord['lon'], coord['uid']):
        congestion_data = get_congestion_data_per_station(str(i),str(j),str(k))
        df = pd.concat([df,congestion_data]) 
        df["time"] = pd.to_datetime(df["time"])
        #df['lat'] = df['lat'].multiply(10000)
    return(df)

def get_url_and_emission_data_for_all_stations():
    url_p1 = 'https://api.waqi.info/feed/@'
    url_p2 = '/?token=6c2f4b6dbe6b2a49226f6969be2dbaa92a187cf8'
    df = pd.DataFrame()
    city_stations = choose_city_by_coordinates(upper_bound, lower_bound)
    lat = city_stations['lat']
    lon = city_stations['lon']
    city_stations = city_stations['uid']

    city_stations = city_stations.values.tolist()
    lat = lat.values.tolist()
    lon = lon.values.tolist()
    #type(city_stations)
    df = pd.DataFrame([])
    df_lat = pd.DataFrame()
    df_lon = pd.DataFrame()
    df_uid = pd.DataFrame([])
    for i,j,k  in zip(city_stations, lat, lon):
        url_list = url_p1 + str(i) + url_p2 
        result = requests.get(url_list)
        dict = json.loads(result.content)
        JSON = dict
        filterJSON = {
        'time': str(JSON['data']['time']['s']),
        'h': str(JSON['data']['iaqi']['h']['v']),
        #'no2': str(JSON['data']['iaqi']['no2']['v']),
        
        'p': str(JSON['data']['iaqi']['p']['v']),
        'pm25': str(JSON['data']['iaqi']['pm25']['v']),
        
        't': str(JSON['data']['iaqi']['t']['v']),
        
            }
        liste = []
        liste.append(filterJSON)
        liste = pd.DataFrame(liste)
        #liste = liste.set_index('time')  
        df = pd.concat([df,liste]) 
        data = j
        data1 = i
        data2 = k
        lat_row = pd.DataFrame([data])
        lon_row = pd.DataFrame([data2])
        uid_row = pd.DataFrame([data1])
        df_lat = pd.concat([df_lat,lat_row]) 
        df_lon = pd.concat([df_lon,lon_row]) 
        df_uid = pd.concat([df_uid, uid_row]) 
        df.set_index('time') 
        df['lat'] = df_lat[0]
        df['lon'] = df_lon[0]
        df['uid'] = df_uid[0]
        df["time"] = pd.to_datetime(df["time"])
        #df.set_index('time') 
    return(df)

left=pd.DataFrame()
right = pd.DataFrame()

def fetch_here():
    
    global left
    global right
    
    data_total_emission1 = get_url_and_emission_data_for_all_stations()
    #data_total_emission1 = data_total_emission1.set_index('time')
    left=left.append(data_total_emission1)
    data_total1 = get_total_congestion_data()
    right=right.append(data_total1)
    #### NAME DATA OUTPUT
    data1 = right.to_csv(congestion_file)
    data2 = left.to_csv(emission_file)
    return(left, right)

schedule.every(1800).seconds.do(fetch_here)

while True:
    try:
        schedule.run_pending()
        time.sleep(0)
        
    except Exception as e:
        print(e)
        print(datetime.datetime.now())
        print('Restarting!')
        schedule.run_pending()



