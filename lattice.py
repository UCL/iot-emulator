#!/usr/bin/python

import requests
import os

class Lattice():
       os.environ["NO_PROXY"] = "*"

       def __init__(self, c_h, c_p):
           self.url = 'http://' + c_h + ':' + c_p

       
       def add_user(self, username, key):
           '''http://localhost:6666/user/?username=uceeftu&type=KEY&token=%2FUsers%2Fuceeftu%2F.ssh%2Fid_rsa'''

           command_url = self.url + '/user/?username=' + username + '&type=KEY&token=' + key
           print(command_url)
           r = requests.post(command_url)
           return r.json()['ID']

     

       def add_host(self, host, port):
           '''http://localhost:6666/host/?hostname=localhost&port=22'''

           command_url = self.url + '/host/?hostname=' + host + '&port=' + port
           print(command_url)
           r = requests.post(command_url)
           return r.json()['ID']



       def create_session(self, host_id, user_id):
           '''http://localhost:6666/session/?host=eef0b718-983d-468b-9fe4-bcf1bb3e2d09&user=0acf8172-c4e4-4a77-afce-a25f568e3d99'''

           command_url = self.url + '/session/?host=' + host_id + '&user=' + user_id
           print(command_url)
           r = requests.post(command_url)
           return r.json()['ID']



       def start_ds(self, session_id, class_name, args):
           '''http://localhost:6666/datasource/?session=58a291b5-7daa-49e0-a3d4-5c507e9a2fb4&class=mon.lattice.appl.datasources.ZMQDataSourceDaemon&args=localhost%2B22998%2Blocalhost%2B6699%2B5555'''

           command_url = self.url + '/datasource/?session=' + session_id + '&class=' + class_name + '&args=' + args
           print(command_url)
           r = requests.post(command_url)
           return r.json()['ID']


       def start_dc(self, session_id, class_name, args):
           command_url = self.url + '/dataconsumer/?session=' + session_id + '&class=' + class_name + '&args=' + args
           print(command_url)
           r = requests.post(command_url)
           return r.json()['ID']


       def load_probe(self, datasource, class_name, args):
           command_url = self.url + '/datasource/' + datasource + '/probe/?className=' + class_name + '&args=' + args
           print(command_url)
           r = requests.post(command_url)
           return r.json()['createdProbeID']


       def load_reporter(self, dataconsumer, class_name, args):
           command_url = self.url + '/dataconsumer/' + dataconsumer + '/reporter/?className=' + class_name + '&args=' + args
           print(command_url)
           r = requests.post(command_url)
           return r.json()['createdReporterID']


       def probe_on(self, probe_id):
           r = requests.put(self.url + '/probe/' + probe_id + '/?status=on')
           return r.json()['success']


       def probe_off(self, probe_id):
           r = requests.put(self.url + '/probe/' + probe_id + '/?status=off')
           return r.json()['success']


       def unload_probe(self, probe_id):
           r = requests.delete(self.url + '/probe/' + probe_id)
           return r.json()['success']
           

       def unload_reporter(self, reporter_id):
           r = requests.delete(self.url + '/reporter/' + reporter_id)
           return r.json()['success']


       def stop_ds(self, ds_id, session_id):
           r = requests.delete(self.url + '/datasource/' + ds_id + '?session=' + session_id)
           return r.json()['success']

       
       def stop_dc(self, dc_id, session_id):
           r = requests.delete(self.url + '/dataconsumer/' + dc_id + '?session=' + session_id)
           return r.json()['success']


       def delete_host(self, host_id):
           r = requests.delete(self.url + '/host/' + host_id)
           return r.json()['success']


       def delete_session(self, session_id):
           r = requests.delete(self.url + '/session/' + session_id)
           return r.json()['success']


       def delete_user(self, user_id):
           r = requests.delete(self.url + '/user/' + user_id)
           return r.json()['success']

