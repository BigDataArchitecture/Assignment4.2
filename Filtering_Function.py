import gcsfs
from pydoc import describe
import pandas as pd
from geopy import distance
import gcsfs


def filtering_distance(lat,lon):
    data = pd.read_csv('/Users/parthshah/Documents/Northeastern/Spring2022/BigDataAnalytics/Assignment3/data/raw/Nowcast_Catalog.csv')
    print(lat,lon)
    distance_list = []
    for i in range(len(data)):
        a = (data['BEGIN_LAT'].iloc[i],data['BEGIN_LON'].iloc[i])
        b = (lat,lon)
        distance_list.append(distance.distance(a,b).miles)
    data['Distance'] = distance_list
    a = data.sort_values(by=['Distance']).iloc[0]
    print(a['Distance'])
    return a['event_id'],a['Distance'],a['BEGIN_LAT'],a['BEGIN_LON']
