#!/usr/bin/python

from faas_experiment import FaaSExperiment
from container_experiment import ContainerExperiment
from experiment import Connector


if __name__ == '__main__':
   connector = Connector()
   connector.initConnections()

   #arraySizes = [4000, 32000, 64000]
   arraySizes = [16000]
   expSetName = '10_consumers'
   
   #duration = 5
   #duration_weights = [1, 4, 8]
   #duration_weights = [7]
   i = 0

   '''
   for arraySize in arraySizes:
       exp3 = ContainerExperiment(connector, expSetName, arraySize, duration*duration_weights[i])
       exp3.start()

       exp1 = FaaSExperiment(connector, expSetName, 'classic', arraySize, duration*duration_weights[i])
       exp1.start()
   
       exp2 = FaaSExperiment(connector, expSetName, 'flask', arraySize, duration*duration_weights[i])
       exp2.start()

       i=i+1
   '''


   exp1 = FaaSExperiment(connector, expSetName, 'classic', 16000, 10)
   exp1.start()

   exp2 = FaaSExperiment(connector, expSetName, 'flask', 16000, 10)
   exp2.start()

   exp3 = ContainerExperiment(connector, expSetName, 16000, 10)
   exp3.start()
