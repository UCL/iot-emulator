#!/usr/bin/python

from experiment import Experiment
import time

class FaaSExperiment(Experiment):
       def __init__(self, conn, setName, faasType, arraySize, duration):
           self.faasType = faasType
           self.arraySize = arraySize
           self.duration = duration
           self.setName = setName
           self.name = 'faas_' + faasType + '_' + str(arraySize)
           Experiment.__init__(self, conn, self.name, self.setName)


       def startOpenFaaS(self):
           command = '/home/uceeftu/faas/openfaas_deploy.sh'
           result = self.clusterMgmHost.sudo(command, pty=True)
           time.sleep(20)
           if result.ok == True:
              print('Started OpenFaaS')


       def stopOpenFaaS(self):
           command = '/home/uceeftu/faas/openfaas_undeploy.sh'
           result = self.clusterMgmHost.sudo(command, pty=True)
           time.sleep(20)
           if result.ok == True:
              print('Stopped OpenFaaS')

           
       def undeployFunctions(self):
           if self.faasType == 'flask':
              command = '/home/uceeftu/faas/undeploy_flask.sh'
           elif self.faasType == 'classic':
              command = '/home/uceeftu/faas/undeploy_classic.sh'
           result = self.clusterMgmHost.run(command)
  

       def deployFunctions(self):
           if self.faasType == 'flask':
              command = '/home/uceeftu/faas/deploy_flask.sh'
           elif self.faasType == 'classic':
              command = '/home/uceeftu/faas/deploy_classic.sh'
           result = self.clusterMgmHost.run(command)


       def startIoT(self):
           if self.faasType == 'classic':
              path = '/home/uceeftu/iot/faas_classic/'
           elif self.faasType == 'flask':
              path = '/home/uceeftu/iot/faas/'

           command = 'java -cp /home/uceeftu/lattice/jars/monitoring-bin-core-2.0.1.jar mon.lattice.appl.demo.iot.IotEmulator ' \
                     + path + 'iot_' + str(self.arraySize) + '.properties ' + str(self.duration) 
           result = self.monHost.run(command)


       def collectServiceLogs(self):
           if self.faasType == 'classic':
              path = '/home/uceeftu/faas/classic-functions'
           elif self.faasType == 'flask':
              path = '/home/uceeftu/faas/flask-functions'
           command = path + '/log_retriever.sh ' + self.setName + '/' + self.name

           # service logs hang when the number of containers for a service is > 1
           # waiting until docker swarm decreases the number of replicas
           time.sleep(60)
           result = self.clusterMgmHost.sudo(command, pty=True)
           if result.ok == True:
              print('Collected service logs') 


       def start(self):
           self.startLattice()
           self.startOpenFaaS()
           self.deployFunctions()
           self.startMon('faas')
           self.startIoT()
           self.stopMon()
           self.collectServiceLogs()
           self.undeployFunctions()
           self.stopOpenFaaS()
           self.stopLattice()
           self.collectLatticeLogs()
           self.collectTimestamp()

