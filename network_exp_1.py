#!/usr/bin/python

from udp_xdr_network_experiment import UDPXDRSimpleNetworkExperiment
from udp_xdr_with_names_network_experiment import UDPXDRWithNamesSimpleNetworkExperiment
from ws_xdr_network_experiment import WSXDRSimpleNetworkExperiment
from ws_xdr_with_names_network_experiment import WSXDRWithNamesSimpleNetworkExperiment
from ws_network_experiment import WSSimpleNetworkExperiment
from rest_network_experiment import RestSimpleNetworkExperiment
from experiment import Connector


if __name__ == '__main__':
   #mon = 'washington'
   mon = 'stanford'

   ### edge should be changed also in the properties file
   #edge = 'methane'
   #edge_if = 'enp1s0f0'

   edge = 'claythree'
   edge_if = 'enp6s4f0'
 
   ### consumer_port should also be changed in the properties file
   consumer_port = '9999'

   ### consumer_url should also be changed in the properties file
   consumer_url = 'reporter'

   receiver = 'clayone'

   connector = Connector(mon, edge, receiver)
   connector.initConnections()

   duration = 60


   # will be created under user's home directory
   #expSetName = 'exps_results/exp_2/with_print'
   #isVerbose = True

   #exp = UDPXDRSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_2/iot_udp_xdr.properties', expSetName, 'xdr_nonames_udp', duration, edge, edge_if, consumer_port, isVerbose)
   #exp.start()

   #exp = UDPXDRWithNamesSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_2/iot_udp_xdr_with_names.properties', expSetName, 'xdr_udp', duration, edge, edge_if, consumer_port, isVerbose)
   #exp.start()

   #exp = WSXDRSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_2/iot_ws_xdr.properties', expSetName, 'xdr_nonames_ws', duration, edge, edge_if, consumer_port, isVerbose)
   #exp.start()

   #exp = WSXDRWithNamesSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_2/iot_ws_xdr_with_names.properties', expSetName, 'xdr_ws', duration, edge, edge_if, consumer_port, isVerbose)
   #exp.start()

   #exp = WSSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_2/iot_ws.properties', expSetName, 'json_ws', duration, edge, edge_if, consumer_port, isVerbose)
   #exp.start()

   #exp = RestSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_2/iot_rest.properties', expSetName, 'json_rest', duration, edge, edge_if, consumer_port, consumer_url, isVerbose)
   #exp.start()



   expSetName = 'exps_results/exp_1/no_print'
   isVerbose = False

   exp = UDPXDRSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_1/iot_udp_xdr.properties', expSetName, 'xdr_nonames_udp', duration, edge, edge_if, consumer_port, isVerbose)
   exp.start()

   exp = UDPXDRWithNamesSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_1/iot_udp_xdr_with_names.properties', expSetName, 'xdr_udp', duration, edge, edge_if, consumer_port, isVerbose)
   exp.start()

   #exp = WSXDRSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_2/iot_ws_xdr.properties', expSetName, 'xdr_nonames_ws', duration, edge, edge_if, consumer_port, isVerbose)
   #exp.start()

   #exp = WSXDRWithNamesSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_2/iot_ws_xdr_with_names.properties', expSetName, 'xdr_ws', duration, edge, edge_if, consumer_port, isVerbose)
   #exp.start()

   #exp = WSSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_2/iot_ws.properties', expSetName, 'json_ws', duration, edge, edge_if, consumer_port, isVerbose)
   #exp.start()

   #exp = RestSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_2/iot_rest.properties', expSetName, 'json_rest', duration, edge, edge_if, consumer_port, consumer_url, isVerbose)
   #exp.start()

