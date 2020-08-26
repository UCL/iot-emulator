import os

class PlotData():        
        def __init__(self, logfile_name, set_dir, set_info):
            self.logfile_name = logfile_name
            self.set_dir = set_dir
            self.graphs_dir = set_dir + '/graphs/'
            self.set_info = set_info
            #self.data_frames = []
            for exp_info in self.set_info:
                print('loading: ' + exp_info['dir'])
                self.load_data(exp_info)
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
            raise NotImplementedError('subclasses must override load_data!')

