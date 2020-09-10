#!/usr/bin/python

from udp_xdr_network_experiment import UDPXDRSimpleNetworkExperiment
from udp_xdr_with_names_network_experiment import UDPXDRWithNamesSimpleNetworkExperiment
from udp_json_network_experiment import UDPJSONSimpleNetworkExperiment
from ws_xdr_network_experiment import WSXDRSimpleNetworkExperiment
from ws_xdr_with_names_network_experiment import WSXDRWithNamesSimpleNetworkExperiment
from ws_json_network_experiment import WSJSONSimpleNetworkExperiment
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

   duration = 1

   # will be created under user's home directory
   expSetName = 'exps_results/exp_3/no_print'
   conf = 2

   '''
   exp = UDPXDRSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_3/iot_udp_xdr.properties', expSetName, 'xdr_udp_nonames', duration, edge, edge_if, consumer_port, conf)
   exp.start()

   exp = UDPXDRWithNamesSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_3/iot_udp_xdr_with_names.properties', expSetName, 'xdr_udp', duration, edge, edge_if, consumer_port, conf)
   exp.start()

   exp = UDPJSONSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_3/iot_udp_json.properties', expSetName, 'json_udp', duration, edge, edge_if, consumer_port, conf)
   exp.start()

   exp = WSXDRSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_3/iot_ws_xdr.properties', expSetName, 'xdr_ws_nonames', duration, edge, edge_if, consumer_port, conf)
   exp.start()

   exp = WSXDRWithNamesSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_3/iot_ws_xdr_with_names.properties', expSetName, 'xdr_ws', duration, edge, edge_if, consumer_port, conf)
   exp.start()
   '''

   n_threads = 1
   isSimpleJSON = False
   exp = WSJSONSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_3/iot_ws.properties', expSetName, 'json_ws', duration, edge, edge_if, consumer_port, conf, isSimpleJSON, n_threads)
   exp.start()

   exp = RestSimpleNetworkExperiment(connector, '/home/uceeftu/iot/network/exp_3/iot_rest.properties', expSetName, 'json_rest', duration, edge, edge_if, consumer_port, consumer_url, conf)
   exp.start()

