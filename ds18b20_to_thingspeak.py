import os
import glob
import time
import urllib.request

myAPI = "9DOL5UNIAUFZJ3B6"
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
  f = open(device_file, 'r')
  lines = f.readlines()
  f.close()
  return lines

def read_temp():
  lines = read_temp_raw()
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = read_temp_raw()
  equals_pos = lines[1].find('t=')
  if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    temp_c = float(temp_string) / 1000.0
    return temp_c

for i in range(100):
  t = read_temp()
  f = urllib.request.urlopen(baseURL +'&field1='+ str(t))
  html = int(f.read())
  print(html, t)
  time.sleep(30)
