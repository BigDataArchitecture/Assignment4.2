import requests
import json
import numpy as np
from matplotlib import pyplot as plt 
import h5py
import pandas as pd
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os
import time
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

import gcsfs
from pydoc import describe
import pandas as pd
from geopy import distance
import gcsfs


from datetime import datetime

# datetime object containing current date and time
 
def filtering_distance(lat,lon):
    data = pd.read_csv('Nowcast_Catalog.csv')
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

def start():
    print("Airflow_Started")
    return "Done"

def done():
    print("Airflow_Done")
    return "Done"


def airflow_function():
  start_time = time.time()
  print("Started:",start_time)
  credentials_dict = {
    #   credits
  }

  credentials = ServiceAccountCredentials.from_json_keyfile_dict(
      credentials_dict
  )
  client = storage.Client(credentials=credentials, project='bigdata-assignment-340502')

  bucket = client.get_bucket('nowcast_api_data')

  data = pd.read_csv('Cache_Events.csv')

  cache_info = {}
  cache_info['Cache_Lat'] = {}
  cache_info['Cache_Lon'] = {}
  cache_info['Nearest_Event'] = {}
  cache_info['Nearest_Lat'] = {}
  cache_info['Nearest_Lon'] = {}
  cache_info['Distance'] = {}
  cache_info['Run_Time'] = {}
  cache_info['Success'] = {}


  for i in range(20):
    lat = data['BEGIN_LAT'].iloc[i]
    print(lat)
    lon = data['BEGIN_LON'].iloc[i]
    print(lon)
    event_id,distance,nearest_lat,nearest_lon = filtering_distance(lat,lon)
    pay_load = {'lat': nearest_lat,'lon': nearest_lon,'distance': 100, 'model': 'mse_and_style','index': 22}
    print(pay_load)
    cache_info['Cache_Lat'][str(i)] = lat
    cache_info['Cache_Lon'][str(i)] = lon
    cache_info['Nearest_Event'][str(i)] = event_id
    cache_info['Nearest_Lat'][str(i)] = nearest_lat
    cache_info['Nearest_Lon'][str(i)] = nearest_lon
    cache_info['Distance'][str(i)] = distance
    cache_info['Run_Time'][str(i)] = datetime.now()

    print("Search for",lat,lon, "Got",event_id,int(distance),nearest_lat,nearest_lon)

    r=requests.get("https://bigdata-assignment-340502.ue.r.appspot.com/nowcast_results/forecast/latlongcache/", params = pay_load)
    output = r.content.decode()
    res = json.loads(output)
    if len(res)> 2:
      event_loc = "ALL_Cache_Data/"+str(event_id)+".png"
      hf1 = h5py.File(event_loc, 'w')
      for j in range(1,13):
        a = np.array(res[str(j-1)])
        plt.subplot(4, 3, j)
        plt.imshow(a[0,:,:])
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        plt.title(str(j)+" hour of image")
      plt.savefig(event_loc)
      print("Uploading data to GCP")
      blob = bucket.blob(str(event_id)+".png")
      blob.upload_from_filename(event_loc)
      print("Upload Done")
      cache_info['Success'][str(i)]  = 1
    else:
      cache_info['Success'][str(i)]  = "No_Data"
        
  cache_log_file = pd.DataFrame.from_dict(cache_info)
  print(cache_log_file)
  name = "Cache_Log_File.csv"
  cache_log_file.to_csv(name)
  blob = bucket.blob("Cache_Log_File.csv")
  blob.upload_from_filename(name)
  print("--- %s seconds ---" % (time.time() - start_time))
  return "Done"


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'concurrency': 1,
    'retries': 0,
    'depends_on_past': False,
}

with DAG('CNN-Training-Pipeline',
         catchup=False,
         default_args=default_args,
         schedule_interval='0 * * * *',
         ) as dag:
    t0_start = PythonOperator(task_id='UploadModels',
                              python_callable=start)
    t1_getdata = PythonOperator(task_id='ScrapeData',
                                python_callable=airflow_function)


t0_start >> t1_getdata