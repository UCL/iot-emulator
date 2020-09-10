#!/usr/bin/python

from network_experiment import SimpleNetworkExperiment
import time
import os
from shutil import copy
from monitoring import Monitoring


class WSJSONSimpleNetworkExperiment(SimpleNetworkExperiment):

       def __init__(self, conn, conf_file, setName, title, duration, consumer_host, tcpdump_if, consumer_port, conf, use_simple, n_threads=0):
           self.consumer_port = consumer_port
           self.conf = conf
           self.use_simple = use_simple
           self.n_threads = n_threads
           SimpleNetworkExperiment.__init__(self, conn, conf_file, setName, title, duration, tcpdump_if, consumer_port)


       def startConsumer(self):
           print('Starting Processing function')
           if self.use_simple:
              self.dc_class = 'WebSocketJSONSimpleDataConsumer'
           else:
              self.dc_class = 'WebSocketJSONDataConsumer'

           # n_threads = 0 is the default (= n processors)
           if self.n_threads > 0:
              command = 'screen -dmS wsConsumer java -cp /home/uceeftu/lattice/jars/monitoring-bin-core-2.0.1.jar mon.lattice.appl.dataconsumers.' + self.dc_class + ' ' + \
                     self.consumer_port + ' ' + str(self.n_threads) + ' ' + str(self.conf)   
     
           else:
              command = 'screen -dmS wsConsumer java -cp /home/uceeftu/lattice/jars/monitoring-bin-core-2.0.1.jar mon.lattice.appl.dataconsumers.' + self.dc_class + ' ' + \
                     self.consumer_port + ' ' + str(self.conf)

  
           print(command)
           result = self.clusterMgmHost.run(command)

           if result.ok == True:
              command = 'pgrep -fn mon.lattice.appl.dataconsumers.' + self.dc_class
              result = self.clusterMgmHost.run(command, hide=True)
              self.consumer_PID = result.stdout.strip()
              print('Consumer successfully started => PID: ' + self.consumer_PID)
           

       def stopConsumer(self):
           print('Stopping Processing function')
           command = 'kill ' + self.consumer_PID
           result = self.clusterMgmHost.run(command)
           if result.ok == True:
              print('Consumer successfully shut down')

