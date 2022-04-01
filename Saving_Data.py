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
from Filtering_Function import filtering_distance

from datetime import datetime

# datetime object containing current date and time
 

def airflow_function():
  start_time = time.time()
  print("Started:",start_time)
  credentials_dict = { 
    # Your token here
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


  for i in range(10):
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
    try:

      r=requests.get("https://bigdata-assignment-340502.ue.r.appspot.com/nowcast_results/forecast/latlongcache/", params = pay_load)
      print(r)
      output = r.content.decode()
      res = json.loads(output)
      if len(res)> 2:
        event_loc = "ALL_Cache_Data/"+str(event_id)+".png"
        print(event_loc)
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
    except:
      print("error")
        
  cache_log_file = pd.DataFrame.from_dict(cache_info)
  print(cache_log_file)
  name = "ALL_Cache_Data/Cache_Log_File.csv"
  cache_log_file.to_csv(name)
  blob = bucket.blob("Cache_Log_File.csv")
  blob.upload_from_filename(name)
  print("--- %s seconds ---" % (time.time() - start_time))
  return "Done"

airflow_function()


