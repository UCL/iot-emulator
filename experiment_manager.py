#!/usr/bin/python

from faas_experiment import FaaSExperiment
from container_experiment import ContainerExperiment
from experiment import Connector


if __name__ == '__main__':
   connector = Connector()
   connector.initConnections()

   arraySizes = [32000, 64000]
   expSetName = 'test_10_3'
   
   duration = 10
   duration_weights = [4, 8]
   i = 0

   '''
   for arraySize in arraySizes:
       #exp3 = ContainerExperiment(connector, expSetName, arraySize, duration*duration_weights[i])
       #exp3.start()

       #exp1 = FaaSExperiment(connector, expSetName, 'classic', arraySize, duration*duration_weights[i])
       #exp1.start()

       exp2 = FaaSExperiment(connector, expSetName, 'flask', arraySize, duration*duration_weights[i])
       exp2.start()

       i=i+1
   '''


   #exp2 = FaaSExperiment(connector, expSetName, 'flask', 4000, 3)
   #exp2.start()

   exp2 = FaaSExperiment(connector, expSetName, 'flask', 64000, 3)
   exp2.start()
