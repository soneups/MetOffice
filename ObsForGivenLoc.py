#!/usr/bin/env python
# Tweet some weather data!

import time
import sys
import metoffer
from twython import Twython

# Define location of api files - recorded in a file - avoids a GitHub slurp for API keys!
keys_file='/home/pi/piweather/metoffice/MetOffer-1.2/keys'
metkeys_file='/home/pi/piweather/metoffice/MetOffer-1.2/apikeysmetoffice.key'

# Read API keys from file
with open(keys_file) as f:
    CONSUMER_KEY = f.readline().strip("\n")
    CONSUMER_SECRET = f.readline().strip("\n")
    ACCESS_KEY = f.readline().strip("\n")
    ACCESS_SECRET = f.readline().strip("\n")

with open(metkeys_file) as f:
    met_api_key = f.readline().strip("\n")
	
# Setup API calls
api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
met = metoffer.MetOffer(met_api_key)
 
# get local weather
def LookupObs( locationdescription, longitude, latitude ):
   weather_observations = met.nearest_loc_obs(float(longitude),float(latitude)) 
   weather_report = metoffer.parse_val(weather_observations)
   weather_data = weather_report.data[len(weather_report.data)-1]
   wind_info = weather_data['Wind Speed']
   wind_direction = weather_data['Wind Direction']
   mph=int(wind_info[0])
   kph=int(mph*1.609344)
   tmpf=int(weather_data['Temperature'][0])*9/5+32
   print (time.strftime("%d/%m/%Y"))+"@"+(time.strftime("%H:%M:%S")) + " - " +locationdescription+": "+str((weather_data['Temperature'][0]))+"c/"+str(tmpf)+"f, Wind speed: "+str(wind_info[0])+wind_info[1]+" "+wind_direction[0]
   api.update_status(status=str(time.strftime("%d/%m/%Y"))+"@"+str(time.strftime("%H:%M:%S")) + " - " +locationdescription+": "+str((weather_data['Temperature'][0]))+"c/"+str(tmpf)+"f, Wind speed: "+str(wind_info[0])+wind_info[1]+" "+wind_direction[0])
   return;

LookupObs( locationdescription="#BrizeNorton", longitude=51.7616, latitude=-1.5779 );   #Brize
LookupObs( locationdescription="#Stornoway", longitude=58.1011, latitude=-4.9899 );     #Stornoway
LookupObs( locationdescription="#Burnhamonsea", longitude=51.2430, latitude=-2.9920 );  #BOS
LookupObs( locationdescription="#Newquay", longitude=50.3995, latitude=-5.1379 );       #Newquay
