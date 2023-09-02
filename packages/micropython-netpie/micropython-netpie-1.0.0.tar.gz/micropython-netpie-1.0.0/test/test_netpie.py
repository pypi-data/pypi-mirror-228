from simple import MQTTClient,MQTTException
from network import WLAN,STA_IF
from time import sleep
import json
import random
import urequests

class NETPIEException(Exception):
    pass

class NETPIE:
    def __init__(self):
        self.hostname = "mqtt.netpie.io"
        self.port = 1883
        self.msg_topic = "@msg/"
        self.shadow_topic = "@shadow/"
        self.client = None
        self.client_id = None
        self.token = None
        self.secret = None

    def set_profile(self, client_id, token=None, secret=None):
        if not isinstance(client_id, str):
            raise NETPIEException("Client ID must be a string.")

        if token is not None and not isinstance(token, str):
            raise NETPIEException("Token must be a string.")

        if secret is not None and not isinstance(secret, str):
            raise NETPIEException("Secret must be a string.")

        self.client_id = client_id
        self.token = token
        self.secret = secret
        self.client = MQTTClient(
        self.client_id, self.hostname, user=self.token, password=self.secret)

    def connect(self):
        if self.client_id is None:
            raise NETPIEException("Client ID must not be None before connecting.")
        
        if self.token is None:
            raise NETPIEException("Token must not be None before connecting.")
        
        if self.secret is None:
            raise NETPIEException("Secret must not be None before connecting.")
        
        try:
            self.client.connect()
        except MQTTException as e:
            raise NETPIEException("Error {}".format(e))
            
        

    def publish(self, topic, data):
        self.client.publish(topic, data)

    def publishShadow(self, unformat_data):
        if not isinstance(unformat_data, dict):
            raise NETPIEException(
                "Data must be a dictionary, but your data type is {}".format(
                    type(unformat_data)
                )
            )
        formatted_data = {"data": unformat_data}
        topic = self.shadow_topic + "data/update"
        self.publish(topic, json.dumps(formatted_data))

    def publishMessage(self, topic, unformat_message):
        if not isinstance(topic, str):
            raise NETPIEException("Topic must be a string.")

        if not topic.startswith("@msg/"):
            topic = "@msg/" + topic

        if isinstance(unformat_message, str):
            self.publish(topic, unformat_message)
        else:
            raise NETPIEException("Data must be a string.")

    def set_callback(self, callback):
        if callable(callback):
            self.client.set_callback(callback)
        else:
            raise NETPIEException("Must provide a valid callback function. Try removing () after the function name.")
    
    def check_message(self):
        self.client.check_msg()

    def subscribe(self, topic):
        if isinstance(topic, str):
            self.client.subscribe(topic)
        else:
            raise NETPIEException("Topic must be a string.")

# Callback Function
def on_message(topic,msg):
    topic,msg = topic.decode('utf8'),msg.decode('utf8')
    print('message from ',topic ,msg)
            
# Network Credential
#ssid = 'iMakeEDU'     
#password = 'imake1234'
ssid = 'PX_SYSTEM_2.4G'
password = 'PX123456789'
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

client = NETPIE()
client.set_profile(client_id,token,secret)
client.set_callback(on_message)
print('Start Connect to Netpie')
client.connect()
print('MQTT Connected!')
client.subscribe('@msg/data')
while True:
    client.check_message()
    #print('test')
#     _data = {"temperature":random.randint(1, 100),
#              "humidity":random.randint(1, 100),
#              "Aceelerometer":{
#                  "X":random.randint(1, 100),
#                  "Y":random.randint(1, 100),
#                  "Z":random.randint(1, 100),
#                  }}
#     client.publishShadow(_data)
    client.publishMessage("@msg/data","Hey This is {}".format(random.randint(1, 100)))
    sleep(1)


        