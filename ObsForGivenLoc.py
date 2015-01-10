#!/usr/bin/env python
# PiWeather Board
# Tweet some weather data!

import time
import smbus
import sys
import metoffer
from twython import Twython

bus = smbus.SMBus(1)                     # for Raspberry Pi version 2
address = 0x4E                           # i2c board address
ver = bus.read_byte_data(address,0x24)   # read the board version

keys_file='/home/pi/piweather/metoffice/MetOffer-1.2/keys'
with open(keys_file) as f:
    CONSUMER_KEY = f.readline().strip("\n")
    CONSUMER_SECRET = f.readline().strip("\n")
    ACCESS_KEY = f.readline().strip("\n")
    ACCESS_SECRET = f.readline().strip("\n")

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

#val = bus.read_i2c_block_data(address,0x2C,0x07)
#press = bus.read_word_data(address,0x47)
#hum = bus.read_byte_data(address,0x43)
#temp = bus.read_byte_data(address,0x42)
#api.update_status(status=str(val[4])+'/'+str(val[5])+'/'+str(val[6])+'@'+str(val[2]).zfill(2)+':'+str(val[1]).zfill(2)+', the pressure is '+str(press)+' hPa, the humidity is '+str(hum)+'%, the internal temperature is '+str(temp)+'c/'+str(temp*9/5+32)+'f')
#print "Posting tweet @"+str(val[2])+':'+str(val[1])
#
# 
# initialize
metkeys_file='/home/pi/piweather/metoffice/MetOffer-1.2/apikeysmetoffice.key'
with open(metkeys_file) as f:
    met_api_key = f.readline().strip("\n")

met = metoffer.MetOffer(met_api_key)
bus = smbus.SMBus(1)                   # for Raspberry Pi version 2
address = 0x4E                         # i2c board address
ver = bus.read_byte_data(address,0x24) # read the board version
 
# get local weather
weather_observations = met.nearest_loc_obs(float(51.7616),float(-1.5779)) #Brize
#Stornoway..weather_observations = met.nearest_loc_obs(float(58.1011),float(-4.9899)) #Near Stornoway
#Newquay...weather_observations = met.nearest_loc_obs(float(50.3995),float(-5.1379)) #Near Newquay
#BOS...weather_observations = met.nearest_loc_obs(float(51.2430),float(-2.9920)) #Near BOS
weather_report = metoffer.parse_val(weather_observations)
weather_data = weather_report.data[len(weather_report.data)-1]
wind_info = weather_data['Wind Speed']
wind_direction = weather_data['Wind Direction']
mph=int(wind_info[0])
kph=int(mph*1.609344)

tmpf=int(weather_data['Temperature'][0])*9/5+32
print "[3649] - Outside temperature: "+str((weather_data['Temperature'][0]))+"c,"+str(tmpf)+"f, Wind speed: "+str(wind_info[0])+wind_info[1]+" "+wind_direction[0]
#print loc

val = bus.read_i2c_block_data(address,0x2C,0x07)
press = bus.read_word_data(address,0x47)
hum = bus.read_byte_data(address,0x43)
temp = bus.read_byte_data(address,0x42)
#api.update_status(status="[3649] - Outside temperature: "+str((weather_data['Temperature'][0]))+"c, Wind speed: "+str(wind_info[0])+wind_info[1]+" "+wind_direction[0])

# need to add date, time and F to the tweet
# 10Dec15 #api.update_status(status=str(val[4])+'/'+str(val[5])+'/'+str(val[6])+'@'+str(val[2]).zfill(2)+':'+str(val[1]).zfill(2)+' - The outside temperature is '+str((weather_data['Temperature'][0]))+'c/'+str(tmpf)+'f, Wind speed: '+str(wind_info[0])+wind_info[1]+"/"+str(kph)+"kph, "+wind_direction[0])
# 10Dec15 print str(val[4])+'/'+str(val[5])+'/'+str(val[6])+'@'+str(val[2]).zfill(2)+':'+str(val[1]).zfill(2)+' - The outside temperature is '+str((weather_data['Temperature'][0]))+'c/'+str(tmpf)+'f, Wind speed: '+str(wind_info[0])+wind_info[1]+"/"+str(kph)+"kph, "+wind_direction[0]
# CurrentC = (weather_data['Temperature'][0])
