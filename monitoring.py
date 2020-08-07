#!/usr/bin/python

from lattice import Lattice


class Monitoring():

    user='uceeftu'
    key='/home/uceeftu/.ssh/id_rsa'

    controller_port_info = '6699'
    controller_port_control = '5555'

    dc_class = 'mon.lattice.appl.dataconsumers.ZMQControllableDataConsumerDaemon'
    dc_port = '32998'
 
    ds_class = 'mon.lattice.appl.datasources.ZMQDataSourceDaemon'

    probe_hostmon_class = 'mon.lattice.appl.demo.iot.HostInfoProbe'
    probe_tcpdump_class = 'mon.lattice.appl.demo.iot.TcpdumpProbe'

    probe_datarate = '5'

    reporter_hostmon_class = 'mon.lattice.appl.demo.iot.HostInfoReporter'
    reporter_hostmon_logfile = '/hostmon.log'
    reporter_tcpdump_class = 'mon.lattice.appl.demo.iot.TcpdumpReporter'
    reporter_tcpdump_logfile = '/tcpdump.log'


    def __init__(self, host, port, exp_path, iot_host, edge_host, edge_tcpdump_if, edge_tcpdump_port, receiver_host):
        self.controller_host=host
        self.controller_port=port
        self.lattice = Lattice(self.controller_host, self.controller_port)

        self.exp_path = exp_path

        self.host_iot=iot_host
        self.host_edge=edge_host
        self.host_receiver=receiver_host

        self.probe_edge_tcpdump_if = edge_tcpdump_if
        self.probe_edge_tcpdump_port = edge_tcpdump_port

        #self.user='uceeftu'
        #self.key='/home/uceeftu/.ssh/id_rsa'

        #self.controller_port_info = '6699'
        #self.controller_port_control = '5555'

        #self.dc_class = 'mon.lattice.appl.dataconsumers.ZMQControllableDataConsumerDaemon'
        #self.dc_port = '32998'
        self.dc_args = Monitoring.dc_port + '+' + self.controller_host + '+' + Monitoring.controller_port_info + '+' +  Monitoring.controller_port_control

        #self.ds_class = 'mon.lattice.appl.datasources.ZMQDataSourceDaemon'
        self.ds_args = self.host_receiver + '+' +  Monitoring.dc_port + '+' + self.controller_host + '+' +  Monitoring.controller_port_info + '+' +  Monitoring.controller_port_control

        #self.probe_hostmon_class = 'mon.lattice.appl.demo.iot.HostInfoProbe'
        #self.probe_tcpdump_class = 'mon.lattice.appl.demo.iot.TcpdumpProbe'

        #self.probe_datarate = '5'

        #self.reporter_hostmon_class = 'mon.lattice.appl.demo.iot.HostInfoReporter'
        #self.reporter_tcpdump_class = 'mon.lattice.appl.demo.iot.TcpdumpReporter'
        self.reporter_hostmon_args = self.exp_path +  Monitoring.reporter_hostmon_logfile
        self.reporter_tcpdump_args = self.exp_path +  Monitoring.reporter_tcpdump_logfile




    def init(self):
        self.user_id = self.lattice.add_user(Monitoring.user, Monitoring.key)

        self.host_iot_id = self.lattice.add_host(self.host_iot, '22')
        self.host_edge_id = self.lattice.add_host(self.host_edge, '22')
        self.host_receiver_id = self.lattice.add_host(self.host_receiver, '22')

        self.host_iot_session = self.lattice.create_session(self.host_iot_id, self.user_id)
        self.host_edge_session = self.lattice.create_session(self.host_edge_id, self.user_id)
        self.host_receiver_session = self.lattice.create_session(self.host_receiver_id, self.user_id)


    def start_components(self):
        self.receiver_dc = self.lattice.start_dc(self.host_receiver_session, Monitoring.dc_class, self.dc_args)
        self.reporter_receiver_hostmon = self.lattice.load_reporter(self.receiver_dc, Monitoring.reporter_hostmon_class, self.reporter_hostmon_args)
        self.reporter_receiver_tcpdump = self.lattice.load_reporter(self.receiver_dc, Monitoring.reporter_tcpdump_class, self.reporter_tcpdump_args)

        self.iot_ds = self.lattice.start_ds(self.host_iot_session, Monitoring.ds_class, self.ds_args)
        self.edge_ds = self.lattice.start_ds(self.host_edge_session, Monitoring.ds_class, self.ds_args)

        iot_hostmon_args = self.host_iot + '+' + Monitoring.probe_datarate
        self.probe_iot_hostmon = self.lattice.load_probe(self.iot_ds, Monitoring.probe_hostmon_class, iot_hostmon_args)

        #iot_tcpdump_args = self.host_iot + '+' + self.probe_iot_tcpdump_if + '+' + self.probe_iot_tcpdump_port + '+' + Monitoring.probe_datarate
        #self.probe_iot_tcpdump = self.lattice.load_probe(self.iot_ds, Monitoring.probe_tcpdump_class, iot_tcpdump_args)

        edge_hostmon_args = self.host_edge + '+' + Monitoring.probe_datarate
        self.probe_edge_hostmon = self.lattice.load_probe(self.edge_ds, Monitoring.probe_hostmon_class, edge_hostmon_args)

        edge_tcpdump_args = self.host_edge + '+' + self.probe_edge_tcpdump_if + '+' + self.probe_edge_tcpdump_port + '+' + Monitoring.probe_datarate
        self.probe_edge_tcpdump = self.lattice.load_probe(self.edge_ds, Monitoring.probe_tcpdump_class, edge_tcpdump_args)

        

    def start_monitoring(self):
        self.lattice.probe_on(self.probe_iot_hostmon)
        #self.lattice.probe_on(self.probe_iot_tcpdump)
        self.lattice.probe_on(self.probe_edge_hostmon)
        self.lattice.probe_on(self.probe_edge_tcpdump)


    def stop_monitoring(self):
        self.lattice.probe_off(self.probe_iot_hostmon)
        #self.lattice.probe_off(self.probe_iot_tcpdump)
        self.lattice.probe_off(self.probe_edge_hostmon)
        self.lattice.probe_off(self.probe_edge_tcpdump)


    def stop_components(self):
        self.lattice.unload_probe(self.probe_iot_hostmon)
        #self.lattice.unload_probe(self.probe_iot_tcpdump)
        self.lattice.unload_probe(self.probe_edge_hostmon)
        self.lattice.unload_probe(self.probe_edge_tcpdump)

        self.lattice.stop_ds(self.iot_ds, self.host_iot_session)
        self.lattice.stop_ds(self.edge_ds, self.host_edge_session)

        self.lattice.unload_reporter(self.reporter_receiver_hostmon)
        self.lattice.unload_reporter(self.reporter_receiver_tcpdump)
        self.lattice.stop_dc(self.receiver_dc, self.host_receiver_session)


    def cleanup(self):
        self.lattice.delete_session(self.host_iot_session)
        self.lattice.delete_session(self.host_edge_session)
        self.lattice.delete_session(self.host_receiver_session)

        self.lattice.delete_host(self.host_iot_id)
        self.lattice.delete_host(self.host_edge_id)
        self.lattice.delete_host(self.host_receiver_id)

        self.lattice.delete_user(self.user_id)

