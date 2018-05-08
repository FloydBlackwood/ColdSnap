#08/05/2018
#@author Ian Marshall 17132207

import tweepy
from credentials import *
import time
import grovepi
import subprocess
import math
import random
import os

#digital sensor
dht_sensor_port = 7
dht_sensor_type = 0

#create tweepy object using access keys
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#tried to create a folder of images that would be randomly selected but kept getting errors
#path = r"/home/pi/coldsnap/images"
#image = random.choice([x for x in os.listdir("path")if os.path.isfile(os.path.join("path",x))])

#image to tweet with temperature readings
image = '/home/pi/coldsnap/shining.jpg'

#set threshold. if temperature drops below threshold alert is sent to twitter
threshold = 20.00

#get list of followers from twitter
users = tweepy.Cursor(api.followers, screen_name="floydblackwood").items()

#set time increment
time_to_sleep = 3600

#create csv file to log sensor readings
log_file = "coldsnap_log.csv"


#def read_sensor()
#08/05/2018
#@reference https://github.com/DexterInd/GrovePi/blob/master/Projects/plant_monitor/plant_project.py
#@author Ian Marshall 17132207

#Read the data from the sensors
def read_sensor():
    try:
        [temp,humidity] = grovepi.dht(dht_sensor_port,dht_sensor_type)
        #Return -1 in case of bad temperature or humidity sensor reading
        if math.isnan(temp) or math.isnan(humidity):
            return [-1,-1]
        return [temp,humidity]

    #Return -1 in case of sensor error
    except IOError as TypeError:
            return [-1,-1]

while True:
    curr_time_sec=int(time.time())
    #print list of followers received from twitter
    for user in users:
        print("@" + user.screen_name)
    # If it is time to take the sensor reading
    if curr_time_sec>1:
        [temp,humidity]=read_sensor()
        # If any reading is a bad reading, skip the loop and try again
        if temp==-1:
            print("Bad reading")
            time.sleep(1)
            continue
        curr_time = time.strftime("%Y-%m-%d:%H-%M-%S")
        print(("Time:%s\nTemp: %.2f C\nHumidity:%.2f %%\n" %(curr_time,temp,humidity)))
         
        # Save the sensor reading to the CSV file
        f=open(log_file,'a')
        f.write("%s,%.2f,%.2f;\n" %(curr_time,temp,humidity))
        f.close()
        if temp < threshold:
             api.update_with_media(image, status="Time:%s\nIt's only %.2f Degrees Celsius here\nCheck that I'm still okay\n" %(curr_time,temp))
     
    #Slow down the loop
    time.sleep(time_to_sleep)
