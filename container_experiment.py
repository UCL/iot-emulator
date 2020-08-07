#!/usr/bin/python

from experiment import Experiment
import time

class ContainerExperiment(Experiment):
       def __init__(self, conn, setName, arraySize, duration):
           self.arraySize = arraySize
           self.duration = duration
           self.setName = setName
           self.name = 'micro_' + str(arraySize)
           Experiment.__init__(self, conn, self.name, self.setName)
 

       def undeployContainers(self):
           command = '/home/uceeftu/microservices/microservices_flask/undeploy.sh'
           result = self.clusterMgmHost.sudo(command, pty=True)
           time.sleep(10)
           if result.ok == True:
              print('Stopped microservices')


       def deployContainers(self):
           command = '/home/uceeftu/microservices/microservices_flask/deploy.sh'
           result = self.clusterMgmHost.sudo(command, pty=True)
           time.sleep(10)       
           if result.ok == True:
              print('Started microservices')
    

       def startIoT(self):
           path = '/home/uceeftu/iot/containers/'
           command = 'java -cp /home/uceeftu/lattice/jars/monitoring-bin-core-2.0.1.jar mon.lattice.appl.demo.iot.IotEmulator ' \
                     + path + 'iot_' + str(self.arraySize) + '.properties ' + str(self.duration) 
           result = self.monHost.run(command)


       def collectServiceLogs(self):
           command = '/home/uceeftu/microservices/microservices_flask/log_retriever.sh ' + self.setName + '/' + self.name
           result = self.clusterMgmHost.sudo(command, pty=True)
           if result.ok == True:
              print('Collected service logs')


       def start(self):
           self.startLattice()
           self.deployContainers()
           self.startMon('micro')
           self.startIoT()
           self.stopMon()
           self.collectServiceLogs()
           self.undeployContainers()
           self.stopLattice()
           self.collectLatticeLogs()
           self.collectTimestamp()

