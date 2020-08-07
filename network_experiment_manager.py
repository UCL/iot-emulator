#!/usr/bin/python

from ws_network_experiment import WSSimpleNetworkExperiment
from rest_network_experiment import RestSimpleNetworkExperiment
from experiment import Connector


if __name__ == '__main__':
   #mon = 'washington'
   mon = 'stanford'

   #edge = 'methane'
   #edge_if = 'enp1s0f0'

   ### edge should be changed also in the properties file
   edge = 'claythree'
   edge_if = 'enp6s4f0'
 
   ### consumer_port should also be changed in the properties file
   consumer_port = '9999'

   ### consumer_url should also be changed in the properties file
   consumer_url = 'reporter'

   receiver = 'clayone'

   connector = Connector(mon, edge, receiver)
   connector.initConnections()

   expSetName = 'test'
   
   duration = 10

   exp = WSSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/iot_ws.properties', expSetName, duration, edge, edge_if, consumer_port)
   exp.start()

   exp = RestSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/iot_rest.properties', expSetName, duration, edge, edge_if, consumer_port, consumer_url)
   exp.start()

