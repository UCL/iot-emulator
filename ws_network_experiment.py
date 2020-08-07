#!/usr/bin/python

from network_experiment import SimpleNetworkExperiment
import time
import os
from shutil import copy
from monitoring import Monitoring


class WSSimpleNetworkExperiment(SimpleNetworkExperiment):
       def __init__(self, conn, conf_file, setName, duration, consumer_host, tcpdump_if, consumer_port):
           self.consumer_host = consumer_host
           self.consumer_port = consumer_port
           SimpleNetworkExperiment.__init__(self, conn, conf_file, setName, duration, tcpdump_if, consumer_port)
 

       def startConsumer(self):
           print('Starting Processing function')
           command = 'screen -dmS wsConsumer java -cp /home/uceeftu/lattice/jars/monitoring-bin-core-2.0.1.jar mon.lattice.appl.dataconsumers.WebSocketDataConsumer ' + self.consumer_port
           result = self.clusterMgmHost.run(command)

           if result.ok == True:
              command = 'screen -list | grep wsConsumer'
              result = self.clusterMgmHost.run(command, hide=True)
              self.consumer_PID = result.stdout.strip().split('.')[0].strip()
              print('Consumer successfully started => PID: ' + self.consumer_PID)
           

       def stopConsumer(self):
           print('Stopping Processing function')
           command = 'kill ' + self.consumer_PID
           result = self.clusterMgmHost.run(command)
           if result.ok == True:
              print('Consumer successfully shut down')

