import os
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class PlotNetworkData():

        def __init__(self, logfile_name, set_dir, dirs):
            self.set_dir = set_dir
            self.graphs_dir = set_dir + '/graphs/'
            self.dirs = dirs
            self.data_frames = []
            for exp_dir in self.dirs:
                print('loading: ' + exp_dir)
                self.load_data(exp_dir + '/' + logfile_name)
            self.__create_dir()



        def __create_dir(self):
            if not os.path.isdir(self.graphs_dir):
               try:
                  os.mkdir(self.graphs_dir)
               except OSError:
                  print('Error while creating graphs directory')
                  exit(1)


        def get_title(self, directory):
            f = open(directory + '/title.txt')
            title = f.readline()
            f.close()
            return title.strip()
	    

        def load_data(self, file_name):
            data_frame = pd.read_csv(file_name,
                                          sep = ' ',
                                          names=['Timestamp', 'Elapsed', 'Type', 'Name', 'Interface', 'Port', 'inBytes', 'inPackets', 'outBytes', 'outPackets'])
            data_frame['Elapsed'] = pd.to_timedelta(data_frame['Elapsed'])
            #print(data_frame.tail())
            self.data_frames.append(data_frame)


        def plot_bytes(self):
            fig, (ax1, ax2) = plt.subplots(2, 1, sharey=True)

            dir_index = 0
            for data_frame in self.data_frames:
                x = data_frame.Elapsed.dt.total_seconds()
                y1 = data_frame.inBytes
                y2 = data_frame.outBytes
                label = self.get_title(self.dirs[dir_index])
                ax1.plot(x, y1, label=label)
                ax2.plot(x, y2, label=label)
                dir_index+=1

            # adjusting the ticks on the xasis to match time base (60)
            stepsize = 600
            start = x.min()
            end = x.max()
 
            ax1.xaxis.set_ticks(np.arange(start, end, stepsize))
            ax2.xaxis.set_ticks(np.arange(start, end, stepsize))

            ax1.set(xlabel='elapsed time (s)', 
                   ylabel='number of bytes', 
                   title='Received bytes (on Edge host)')

            ax2.set(xlabel='elapsed time (s)',
                   title='Reply bytes (from Edge host)')

            ax1.grid()
            ax1.legend(loc='upper left', fontsize='xx-small')
            ax1.ticklabel_format(axis='y', scilimits=(9,9), useMathText=True)

            ax2.grid()
            ax2.legend(loc='upper left', fontsize='xx-small')

            fig.tight_layout() 
            fig.savefig(self.graphs_dir + "/bytes.pdf")
            

        def plot_packets(self):
            fig, (ax1, ax2) = plt.subplots(2, 1, sharey=True)
            dir_index = 0
            for data_frame in self.data_frames:
                x = data_frame.Elapsed.dt.total_seconds()
                y1 = data_frame.inPackets
                y2 = data_frame.outPackets
                label = self.get_title(self.dirs[dir_index])
                ax1.plot(x, y1, label=label)
                ax2.plot(x, y2, label=label)
                dir_index+=1

            # adjusting the ticks on the xasis to match time base (60)
            stepsize = 600
            start = x.min()
            end = x.max()

            ax1.xaxis.set_ticks(np.arange(start, end, stepsize))
            ax2.xaxis.set_ticks(np.arange(start, end, stepsize))

            ax1.set(xlabel='elapsed time (s)',
                   ylabel='number of packets',
                   title='Received packets (on Edge host)')

            ax2.set(xlabel='elapsed time (s)',
                   ylabel='number of packets',
                   title='Reply packets (from Edge host)')

            ax1.grid()
            ax1.legend(loc='upper left', fontsize='xx-small')
            ax1.ticklabel_format(axis='y', scilimits=(9,9), useMathText=True)

            ax2.grid()
            ax2.legend(loc='upper left', fontsize='xx-small')

            fig.tight_layout()
            fig.savefig(self.graphs_dir + "/packets.pdf")



if __name__ == '__main__':
   dirs = [f.path for f in os.scandir('/home/uceeftu/exps_results/exp_1/with_print') if f.is_dir() and 'exp' in f.name]
   p = PlotNetworkData('tcpdump.log', '/home/uceeftu/exps_results/exp_1/with_print', dirs)
   p.plot_bytes()
   p.plot_packets()
   
