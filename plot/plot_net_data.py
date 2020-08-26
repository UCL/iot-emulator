from plot_data import PlotData

import os
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class PlotNetworkData(PlotData):

        def __init__(self, logfile_name, set_dir, dirs):
            PlotData.__init__(self, logfile_name, set_dir, dirs)


        def load_data(self, exp_info):
            file_name = exp_info['dir'] + '/' + self.logfile_name

            data_frame = pd.read_csv(file_name,
                                          sep = ' ',
                                          names=['Timestamp', 'Elapsed', 'Type', 'Name', 'Interface', 'Port', 'inBytes', 'inPackets', 'outBytes', 'outPackets'])
            data_frame['Elapsed'] = pd.to_timedelta(data_frame['Elapsed'])
            #print(data_frame.tail())
            exp_info['data'] = data_frame


        def plot_bytes(self):
            fig, (ax1, ax2) = plt.subplots(2, 1, sharey=True)

            for exp_info in self.set_info:
                data_frame = exp_info['data']

                x = data_frame.Elapsed.dt.total_seconds()
                y1 = data_frame.inBytes
                y2 = data_frame.outBytes

                label = exp_info['title']
                ax1.plot(x, y1, label=label)
                ax2.plot(x, y2, label=label)

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
            for exp_info in self.set_info:
                data_frame = exp_info['data']
                x = data_frame.Elapsed.dt.total_seconds()
                y1 = data_frame.inPackets
                y2 = data_frame.outPackets
                label = exp_info['title']
                ax1.plot(x, y1, label=label)
                ax2.plot(x, y2, label=label)

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
            ax1.ticklabel_format(axis='y', scilimits=(6,6), useMathText=True)

            ax2.grid()
            ax2.legend(loc='upper left', fontsize='xx-small')

            fig.tight_layout()
            fig.savefig(self.graphs_dir + "/packets.pdf")



if __name__ == '__main__':
   dirs = [f.path for f in os.scandir('/home/uceeftu/exps_results/exp_1/with_print') if f.is_dir() and 'exp' in f.name]
   p = PlotNetworkData('tcpdump.log', '/home/uceeftu/exps_results/exp_1/with_print', dirs)
   p.plot_bytes()
   p.plot_packets()
   
