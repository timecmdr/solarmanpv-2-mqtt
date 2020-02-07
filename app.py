#!/usr/bin/python3

import os
import time, json
import paho.mqtt.publish as publish
import urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse, hashlib
from xml.etree import ElementTree as ET

mqtt_broker = "10.0.3.11"

#config
username            = '' #your portal username [= email-address]
password            = '' #your portal password
baseURL             = 'http://www.solarmanpv.com:10000' #base url
stationid           = '88533' #station id, get this via the station python script
mqtt_broker         = "10.0.3.11" #Location of MQTT Broker

# Working base urls:
#       http://www.ginlongmonitoring.com:10000/
#       http://www.omnikportal.com:10000/
#       http://log.trannergy.com:10000/
#       http://www.solarmanpv.com:10000/
# Line 16

m = hashlib.md5()
m.update(password.encode('utf-8'))


#building url
requestURL = baseURL+'/serverapi/?method=Login&username='+username+'&password='+m.hexdigest()+'&key=apitest&client=iPhone'
#print (requestURL)

#login call
try:
  root = ET.parse(urllib.request.urlopen(requestURL,timeout=10)).getroot()
  token = root.find('token').text
  print(('Logged In: '+username))

except urllib.request.urlerror as e:
  print ('Not logged in: ERROR')
  print (e)
  exit()

#info url
infoURL = baseURL+'/serverapi/?method=Powerstationslist&username='+username+'&token='+token+'&key=apitest'


print ('Getting station id(s)... ')

#login call
infoRoot = ET.parse(urllib.request.urlopen(infoURL)).getroot()
for elem in infoRoot.findall('power'):
    print(("StationID: "+elem.find('stationID').text))


#find data
power = infoRoot.find('power')

#get data
ActualPower = power.find('ActualPower').text
etoday = power.find('etoday').text
etotal = power.find('etotal').text
TotalIncome = power.find('TotalIncome').text

#convert
ActualPower1000 = float(ActualPower) / float ('1000.0')
etotal1000 = float(etotal) / float('1000.0')
etotalfloat = float(etotal)
etotal1000str=str(round(etotal1000,2))
etotalstr= str(round(etotalfloat,2))
actualpowerstr=str(round(ActualPower1000,2))

#logging values
#print ('ActualPower kW: '+actualpowerstr)
#printv(ActualPower)
#print ('etoday kWh: '+etoday)
#print ('etotal KWh: '+etotalstr)
#print ('etotal MWh: '+etotal1000str)

values = {
            "ActualPowerKw": actualpowerstr,
            "ActualPower": ActualPower, 
            "etoday_KWh": etotal,
            "etotal_KWh": etotal,
            "etotal_MWh": etotal1000str
        } 
json_output = json.dumps(values)

publish.single("home/solarmanpv", json_output, hostname=mqtt_broker)
