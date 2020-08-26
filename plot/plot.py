import os
import bisect
from plot_net_data import PlotNetworkData
from plot_consumer_data import PlotConsumerData

class Plot():
      def __init__(self, exp_set):
          self.exp_set = exp_set
          self.__sort_exps_dirs(self.__scan_dir())


      def __scan_dir(self):
          return [f.path for f in os.scandir(self.exp_set) if f.is_dir() and 'exp' in f.name]
          

      def __sort_exps_dirs(self, unsorted_dirs_list):
          # the actual list with info
          sorted_dirs_info_list = []

          # a support list used to sort info based on titles
          sorted_titles_list = []

          for exp_dir in unsorted_dirs_list:
              f = open(exp_dir + '/title.txt')
              title = f.readline().strip()
              
              exp_info = {}
              exp_info['dir'] = exp_dir
              exp_info['title'] = title 

              # we find the insertion point based on title
              position = bisect.bisect(sorted_titles_list, title)
              # insertion in the support list
              sorted_titles_list.insert(position, title)

              # insertion of the actual information
              sorted_dirs_info_list.insert(position, exp_info)
              
          f.close()
          self.exp_set_info = sorted_dirs_info_list
          


      def plot_network(self):
          pnd = PlotNetworkData('tcpdump.log', self.exp_set, self.exp_set_info)
          pnd.plot_bytes()
          pnd.plot_packets()


      def plot_consumer(self):
          pcd = PlotConsumerData('consumerproc.log', self.exp_set, self.exp_set_info)
          pcd.plot()
          pcd.plot_bars()


if __name__ == '__main__':
   p = Plot('/home/uceeftu/exps_results/exp_1/with_print')
   p.plot_network()
   p.plot_consumer()

