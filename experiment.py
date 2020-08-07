#!/usr/bin/python

from fabric import Connection, Config
import getpass
import time

class Connector:
       def __init__(self, mon = 'washington', cluster = 'methane', receiver = None):
           self.monHostName = mon
           self.clusterMgmHostName = cluster
           self.receiverHostName = receiver

       def getPass(self):
           sudoPass = getpass.getpass('Insert Password: ')
           return Config(overrides={'sudo': {'password': sudoPass}})
      
       def initConnections(self):
           passConfig = self.getPass()
           self.monHost = Connection(self.monHostName, config=passConfig)
           self.clusterMgmHost = Connection(self.clusterMgmHostName, config=passConfig)
           if self.receiverHostName is not None:
              self.receiverHost = Connection(self.receiverHostName, config=passConfig)
           

class Experiment:
       def __init__(self, conn, name, setName):
           self.monHost = conn.monHost
           self.clusterMgmHost = conn.clusterMgmHost
           self.name = name
           self.setName = setName
           self.latticeCtrlPID = None
           self.monPID = None
           self.exp_path = '/home/uceeftu/lattice-integration-FaaS/script_prometheus_query/metrics/' + self.setName + '/' + self.name

       def startLattice(self):
           command = 'screen -dmS lattice java -cp /home/uceeftu/lattice/jars/monitoring-bin-controller-2.0.1.jar mon.lattice.control.controller.json.ZMQController'
           result = self.monHost.run(command)
           if result.ok == True:
              command = 'screen -list | grep lattice'
              result = self.monHost.run(command, hide=True)
              self.latticeCtrlPID = result.stdout.strip().split('.')[0].strip()
              time.sleep(1)
              print('Lattice controller successfully started => PID: ' + self.latticeCtrlPID)


       def stopLattice(self):
           command = 'kill ' + self.latticeCtrlPID
           result = self.monHost.run(command)
           if result.ok == True:
              print('Lattice Controller successfully shut down')


       def removeDataConsumers(self):
           command = 'pkill -9 -f DataConsumerDaemon'
           result = self.monHost.run(command)
           if result.ok == True:
              print('Killed existing Data Consumers')


       def startMon(self, containerType):
           promHost = 'methane'
           promPort = '9090'
           promFaaSPort = '9091'
           waitFor = '10' #secs
           
           command = 'screen -dmS mon python /home/uceeftu/lattice-integration-FaaS/script_prometheus_query/metrics.py ' \
                     + promHost + ' ' + promPort + ' ' + promFaaSPort + ' ' + waitFor + ' ' + containerType + ' ' + self.setName + '/' + self.name

           print(command)

           result = self.clusterMgmHost.run(command)
           if result.ok == True:
              command = 'screen -list | grep mon'
              result = self.clusterMgmHost.run(command, hide=True)
              self.monPID = result.stdout.strip().split('.')[0].strip()
              print('Monitoring successfully started => PID: ' + self.monPID)

 
       def stopMon(self):
           command = 'kill ' + self.monPID
           result = self.clusterMgmHost.run(command)
           if result.ok == True:
              print('Monitoring successfully shut down')


       def collectLatticeLogs(self):
           directory = self.exp_path + '/dc/'
           command = 'mkdir ' + directory
           result = self.monHost.run(command)
           if result.ok == True:
              command = 'cp /tmp/data-consumer-* ' + directory
              result = self.monHost.run(command)
              if result.ok == True:
                 command = 'rm /tmp/data-*'
                 #command = 'rm /tmp/data-consumer-*'
                 result = self.monHost.run(command)
                 if result.ok == True:
                    print('Successfully imported  dc logs')


       def collectTimestamp(self):
           directory = self.exp_path + '/'
           command = 'mv /tmp/timestamp-*.log ' + directory
           result = self.monHost.run(command)
           if result.ok == True:
              print('Successfully imported IoT emulator timestamp information')
