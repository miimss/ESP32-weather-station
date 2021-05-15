import network
import time
from machine import Pin
import dht
import urequests
import secrets

sensor = dht.DHT11(Pin(12, Pin.IN, Pin.PULL_UP))

def do_connect():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  print(wlan.scan())
  if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
    while not wlan.isconnected():
      time.sleep_ms(500)
      pass
  print('network config:', wlan.ifconfig())

def read_sensor():
  global temp, hum
  temp = hum = 0
  try:
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
      msg = {"temp": temp, "hum": hum}

      hum = round(hum, 2)
      
      print(msg)
    else:
      print('Invalid sensor readings.')
  except OSError as e:
    print('Failed to read sensor.')

do_connect()

while True:   
  read_sensor()

  my_URL = ('http://dweet.io/dweet/for/minnan-weather?temp={}&hum={}'.format(temp, hum))
  print(my_URL)
  
  try:
    response = urequests.post(my_URL)
    print(response)
  except:
    pass
    
  time.sleep(30)
