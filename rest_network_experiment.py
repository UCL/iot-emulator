#!/usr/bin/python

from network_experiment import SimpleNetworkExperiment
import time
import os
from shutil import copy
from monitoring import Monitoring


class RestSimpleNetworkExperiment(SimpleNetworkExperiment):
       def __init__(self, conn, conf_file, setName, title, duration, consumer_host, tcpdump_if, consumer_port, consumer_url, conf, n_threads=0):
           self.consumer_host = consumer_host
           self.consumer_port = consumer_port
           self.consumer_url = consumer_url
           self.conf = conf
           self.n_threads = n_threads
           SimpleNetworkExperiment.__init__(self, conn, conf_file, setName, title, duration, tcpdump_if, consumer_port)
 

       def startConsumer(self):
           print('Starting Processing function')
           consumer_path = '/home/uceeftu/lattice/'

           if self.n_threads > 0:
              command = 'screen -dmS restConsumer java -cp ' + \
                        consumer_path + '/jars/monitoring-bin-core-2.0.1.jar' + ':' + \
                        consumer_path + '/libs/controller/simple-4.1.21.jar ' + \
                        'mon.lattice.appl.dataconsumers.RestDataConsumer ' + self.consumer_port + ' ' + self.consumer_url + ' ' + str(self.n_threads) + ' ' + str(self.conf) 
           else:
              command = 'screen -dmS restConsumer java -cp ' + \
                        consumer_path + '/jars/monitoring-bin-core-2.0.1.jar' + ':' + \
                        consumer_path + '/libs/controller/simple-4.1.21.jar ' + \
                        'mon.lattice.appl.dataconsumers.RestDataConsumer ' + self.consumer_port + ' ' + self.consumer_url + ' ' + str(self.conf)

           print(command)
           result = self.clusterMgmHost.run(command)

           if result.ok == True:
              command = 'pgrep -fn mon.lattice.appl.dataconsumers.RestDataConsumer'
              result = self.clusterMgmHost.run(command, hide=True)
              self.consumer_PID = result.stdout.strip()
              print('Consumer successfully started => PID: ' + self.consumer_PID)


       def stopConsumer(self):
           print('Stopping Processing function')
           command = 'kill ' + self.consumer_PID
           result = self.clusterMgmHost.run(command)
           if result.ok == True:
              print('Consumer successfully shut down')

