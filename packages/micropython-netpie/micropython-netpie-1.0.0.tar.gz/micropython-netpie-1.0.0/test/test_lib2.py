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

client_id1 = 'b36d57dd-7a74-44a0-be2e-88a643b41b60'
token1 = 'LFMmCBeNuK5wrC1sj2qt5gfNKAf5s6Yb'
secret1 = '5ikhwLpwNg8KkYWEPf9tvrGTuHhwRgVX'

client_id2 = '97ed6b64-a375-49d6-b3c9-54a6186ec70a'
token2 = '8enGkLCAS9oVrDLoC5kRM976P6GYCJNP'
secret2 = '6dAr7N1Py5zTfUKRoRHGLJ75oznBurzf'

payload = {
        "Temperature": 111,
        "Humidity": 119
}

client = NETPIE()
client.set_profile(client_id2,token2,secret2)
client.publish_device_message("data1","Hello")
client.publish_private_message("device/data1","Hi")
#print(client.write_device_shadow(payload))
#print(client.merge_device_shadow(payload))
#client.set_profile(client_id,token,secret)
#print(client.get_device_shadow(client_id1,token1))
#print(client.get_device_shadow(client_id2,token2))
# print(client.publish_device_message("device/data1","Test3zz"))
