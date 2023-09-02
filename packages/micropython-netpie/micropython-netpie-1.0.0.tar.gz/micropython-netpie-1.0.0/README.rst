MicroPython NETPIE
==================

|Version| |License|

Description
-----------

This Python library provides a convenient way to interact with the
NETPIE IoT platform using both MQTT and REST API. NETPIE is an Internet
of Things (IoT) platform that offers tools and services for connecting
and managing IoT devices.

The library encapsulates functionalities to publish messages, manage
device shadows, subscribe to topics, and more. It aims to simplify the
process of integrating NETPIE's features into your IoT projects.

Features
--------

-  Connect and disconnect from the NETPIE MQTT broker
-  Publish messages and device shadows using MQTT
-  Subscribe to topics and handle incoming MQTT messages
-  Retrieve device status and shadow data using NETPIE's REST API
-  Publish private and device messages using REST API

API Documentation
-----------------

https://github.com/PerfecXX/MicroPython-NETPIE

Example Usage
-------------

-  `Connect to
   NETPIE <https://github.com/PerfecXX/MicroPython-NETPIE/blob/main/doc/MQTT/MQ_01_connection_to_netpie.md>`__
-  `Publish the data to NETPIE with Shadow
   Topic <https://github.com/PerfecXX/MicroPython-NETPIE/blob/main/doc/MQTT/MQ_02_pub_data_shadow.md>`__
-  `Publishing data between the devices with Message
   Topic <https://github.com/PerfecXX/MicroPython-NETPIE/blob/main/doc/MQTT/MQ_03_pub_sub_message.md>`__
-  `Control your device with NETPIE's
   Dashboard. <https://github.com/PerfecXX/MicroPython-NETPIE/blob/main/doc/MQTT/MQ_04_netpie_monitoring.md>`__

.. |Version| image:: https://img.shields.io/badge/version-1.0.0-blue.svg
   :target: https://github.com/yourusername/netpie-python-library
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
