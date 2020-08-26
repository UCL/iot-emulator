import os
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class PlotConsumerData():

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
                                          names=['Timestamp', 'Elapsed', 'Type', 'Name', 'Pid', 'Value'])
            data_frame['Elapsed'] = pd.to_timedelta(data_frame['Elapsed'])
            #print(data_frame.tail())
            self.data_frames.append(data_frame)


        def plot(self):
            fig, (ax1, ax2) = plt.subplots(2, 1)

            dir_index = 0
            for data_frame in self.data_frames:
                cpu = data_frame.loc[data_frame['Type'] == 'C', ['Elapsed', 'Value']]
                mem = data_frame.loc[data_frame['Type'] == 'M', ['Elapsed', 'Value']]
                
                x1 = cpu['Elapsed'].dt.total_seconds()
                y1 = cpu['Value']

                x2 = mem['Elapsed'].dt.total_seconds()
                y2 = mem['Value']
  
                label = self.get_title(self.dirs[dir_index])
                ax1.plot(x1, y1, label=label)
                ax2.plot(x2, y2, label=label)
                dir_index+=1

            # adjusting the ticks on the xasis to match time base (60)
            stepsize = 600

            start = x1.min()
            end = x1.max()
            ax1.xaxis.set_ticks(np.arange(start, end, stepsize))

            start = x2.min()
            end = x2.max()            
            ax2.xaxis.set_ticks(np.arange(start, end, stepsize))

            ax1.set(xlabel='elapsed time (s)', 
                   ylabel='Percentage of total (%)', 
                   title='CPU usage (on Edge host)')

            ax2.set(xlabel='elapsed time (s)',
                   ylabel='Percentage of total (%)',
                   title='Memory usage (on Edge host)')

            ax1.grid()
            ax1.legend(loc='upper left', fontsize='xx-small')

            ax2.grid()
            ax2.legend(loc='upper left', fontsize='xx-small')

            fig.tight_layout() 
            fig.savefig(self.graphs_dir + "/consumer_process.pdf")
            

        def plot_bars(self):
            fig, (ax1, ax2) = plt.subplots(2, 1)

            labels = []

            avgs_cpu = []
            stds_cpu = []
 
            avgs_mem = []
            stds_mem = []

            dir_index = 0
            for data_frame in self.data_frames:
                labels.append(self.get_title(self.dirs[dir_index]))
                dir_index+=1

                avgs_cpu.append(data_frame.groupby('Type')['Value'].get_group('C').mean())
                stds_cpu.append(data_frame.groupby('Type')['Value'].get_group('C').std())

                avgs_mem.append(data_frame.groupby('Type')['Value'].get_group('M').mean())
                stds_mem.append(data_frame.groupby('Type')['Value'].get_group('M').std())
    
            ypos = np.arange(len(labels))

            ax1.bar(ypos, avgs_cpu, yerr=stds_cpu)
            ax2.bar(ypos, avgs_mem, yerr=stds_mem)

            ax1.set(ylabel='Average CPU usage (%)',
                   title='Average CPU usage (on Edge host)')

            ax2.set(ylabel='Average Mem usage (%)',
                   title='Average Mem usage (on Edge host)')

            ax1.xaxis.set_ticks(ypos)
            ax1.xaxis.set_ticklabels(labels, fontsize='x-small')
            ax1.grid()
            ax1.set_axisbelow(True)

            ax2.xaxis.set_ticks(ypos)
            ax2.xaxis.set_ticklabels(labels, fontsize='x-small')
            ax2.grid()
            ax2.set_axisbelow(True)

            fig.tight_layout()
            fig.savefig(self.graphs_dir + "/consumer_process_bar.pdf")




if __name__ == '__main__':
   dirs = [f.path for f in os.scandir('/home/uceeftu/exps_results/exp_1/with_print') if f.is_dir() and 'exp' in f.name]
   p = PlotConsumerData('consumerproc.log', '/home/uceeftu/exps_results/exp_1/with_print', dirs)
   p.plot_bars()
   
