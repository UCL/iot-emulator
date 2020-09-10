#!/usr/bin/python

from experiment import Experiment
import time
import os
import sys
from shutil import copy
from monitoring import Monitoring


class SimpleNetworkExperiment(Experiment):
       def __init__(self, conn, conf_file, setName, title, duration, tcpdump_if, tcpdump_port):
           self.conn = conn
           self.conf_file = conf_file
           self.setName = setName
           self.title = title
           self.duration = duration
           self.tcpdump_if = tcpdump_if
           self.tcpdump_port = tcpdump_port
           self.exp_name = 'exp_' + title + '_' + str(int(time.time()))
           self.mon_controller = self.conn.monHostName
           self.iot = self.conn.monHostName # this is the same host where the Lattice controller id running
           self.edge = self.conn.clusterMgmHostName # the host where the processing functions are (cm in the case of faas / containers)
           self.receiver = self.conn.receiverHostName
           Experiment.__init__(self, conn, self.exp_name, self.setName)
           self.init()
 

       def startIoT(self):
           command = 'java -cp /home/uceeftu/lattice/jars/monitoring-bin-core-2.0.1.jar mon.lattice.appl.demo.iot.IotEmulator ' \
                     + self.conf_file + ' ' + str(self.duration) 
           result = self.monHost.run(command)


       def init(self):
           # create dir: /home/setName/name/
           self.exp_path = os.getenv("HOME") + '/' + self.setName + '/'
           if not os.path.exists(self.exp_path):
              os.makedirs(self.exp_path)

           self.exp_path = self.exp_path + self.exp_name
           os.mkdir(self.exp_path)
 
           print('Starting experiment ' + self.setName + ' / ' + self.exp_name)
           print('Redirecting output to: ' + self.exp_path + '/output.log')
           print('Redirecting error to: ' + self.exp_path + '/error.log')

           self.stdout = sys.stdout
           self.stderr = sys.stderr
           sys.stdout = open(self.exp_path + '/output.log', 'w')
           sys.stderr = open(self.exp_path + '/error.log', 'w')

           #setting exp title in file
           f = open(self.exp_path + '/title.txt', 'w')
           f.write(self.title)
           f.close()

           print('+++ IoT: ' + self.conn.monHostName)
           print('+++ Edge: ' + self.conn.clusterMgmHostName)
           print('+++ Receiver: ' + self.conn.receiverHostName)


       def cleanup(self):
           sys.stdout.close()
           sys.stderr.close()

           sys.stdout = self.stdout
           sys.stderr = self.stderr
           print('Experiment ' + self.exp_path + ' completed')
           

       def startMon(self):
           print('Starting Mon')
           self.monitor = Monitoring(self.mon_controller, '6666', self.exp_path, self.iot, self.edge, self.tcpdump_if, self.tcpdump_port, self.receiver)
           self.monitor.init()
           self.monitor.set_consumer_pid(self.consumer_PID)
           self.monitor.start_components()
           self.monitor.start_monitoring()
           

       def stopMon(self):
           print('Stopping Mon')
           self.monitor.stop_monitoring()
           self.monitor.stop_components()
           self.monitor.cleanup()
           self.__cleanup_tcpdump()

       #we need this until we manage to kill child tcpdump process properly
       def __cleanup_tcpdump(self):
           command = 'killall tcpdump'
           result = self.clusterMgmHost.sudo(command, pty=True)


       def saveIotConf(self):
           # copy iot.properties into setName/name
           print('Saving iot emulator conf file')
           copy(self.conf_file, self.exp_path + '/iot.properties')
 

       def startConsumer():
           raise NotImplementedError('subclasses must override startConsumer!')

       def stopConsumer():
           raise NotImplementedError('subclasses must override stopConsumer!')

 
       def collectLatticeLogs(self):
           directory = self.exp_path + '/ds/'
           command = 'mkdir ' + directory
           result = self.monHost.run(command)
           if result.ok == True:
              command = 'cp /tmp/data-source-* ' + directory
              result = self.monHost.run(command)
              if result.ok == True:
                 print('Successfully imported  ds logs')
           Experiment.collectLatticeLogs(self)


       def collectConsumerStats(self):
           directory = self.exp_path + '/'
           command = 'mv /tmp/stats_*.log ' + directory
           result = self.clusterMgmHost.run(command)
           if result.ok == True:
              print('Successfully imported IoT emulator timestamp information')    



       def start(self):
           self.startLattice()
           self.startConsumer()
           self.startMon()
           self.startIoT()
           self.stopMon()
           self.stopConsumer()
           self.stopLattice()
           self.collectLatticeLogs()
           self.saveIotConf()
           self.collectTimestamp()
           self.collectConsumerStats()
           self.cleanup()

