from netpie import NETPIE

from network import WLAN,STA_IF
from time import sleep
import random

# Network Credential
ssid = 'iMakeEDU'     
password = 'imake1234'
# ssid = 'PX_SYSTEM_2.4G'
# password = 'PX123456789'
# Connect to Network
sta_if = WLAN(STA_IF)
sta_if.active(True)
if not sta_if.isconnected():
   print("Connecting to wifi: ", ssid)
   sta_if.connect(ssid, password)
   while not sta_if.isconnected():
       pass
print("Connection successful")

client_id = '97ed6b64-a375-49d6-b3c9-54a6186ec70a'
token = '8enGkLCAS9oVrDLoC5kRM976P6GYCJNP'
secret = '6dAr7N1Py5zTfUKRoRHGLJ75oznBurzf'

# Callback Function
def on_message(topic,msg):
    topic,msg = topic.decode('utf8'),msg.decode('utf8')
    print('message from ',topic ,msg)

client = NETPIE()
client.set_profile(client_id,token,secret)
print(client.get_device_shadow())
# print(client.get_device_status(client_id,token))
# client.set_profile(client_id,token,secret)
# client.set_callback(on_message)
# print('Start Connect to Netpie')
# client.connect()
# print('MQTT Connected!')
# client.subscribe('@msg/data1',qos=0)
# client.subscribe('@msg/data2',qos=0)
# while True:
#     client.check_message()
#     client.publishMessage("@msg/data1","Hey This is {}".format(random.randint(1, 100)))
#     sleep(1)
#     client.publishMessage("@msg/data2","Hey This is {}".format(random.randint(1, 100)))
#     sleep(1)
    