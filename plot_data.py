import os
from plot_net_data import PlotNetworkData
from plot_consumer_data import PlotConsumerData

class PlotData():
      def __init__(self, exp_set):
          self.exp_set = exp_set
          self.__scan_dir()


      def __scan_dir(self):
          self.exp_set_dirs = [f.path for f in os.scandir(self.exp_set) if f.is_dir() and 'exp' in f.name]


      def plot_network(self):
          pnd = PlotNetworkData('tcpdump.log', self.exp_set, self.exp_set_dirs)
          pnd.plot_bytes()
          pnd.plot_packets()


      def plot_consumer(self):
          pcd = PlotConsumerData('consumerproc.log', self.exp_set, self.exp_set_dirs)
          pcd.plot()


if __name__ == '__main__':
   p = PlotData('/home/uceeftu/exps_results/exp_1/with_print')
   p.plot_network()
   p.plot_consumer()

