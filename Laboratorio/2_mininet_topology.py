#!/usr/bin/python
import os
from functools import partial
from mininet.node import Intf

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch, OVSSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    OVSSwitch13 = partial(OVSSwitch, protocols='OpenFlow13')

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding remote Ryu controller\n' )
    # c0 = net.addController(
    #     name = 'c0',
    #     controller = RemoteController,
    #     ip = '127.0.0.1',
    #     protocol = 'tcp',
    #     port = 6633
    # )Controller

    # info( '*** Adding default controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='192.168.100.177',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')

    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s1.setMAC("00:00:00:00:10:01")
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s2.setMAC("00:00:00:00:10:02")
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s3.setMAC("00:00:00:00:10:03")
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s4.setMAC("00:00:00:00:10:04")
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s5.setMAC("00:00:00:00:10:05")
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s6.setMAC("00:00:00:00:10:06")

    info( '*** Add hosts\n')
    
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.2', mac='00:00:00:00:00:01', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.3', mac='00:00:00:00:00:02', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.4', mac='00:00:00:00:00:03', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.5', mac='00:00:00:00:00:04', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.6', mac='00:00:00:00:00:05', defaultRoute=None)   
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.7', mac='00:00:00:00:00:06', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.8', mac='00:00:00:00:00:07', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.9', mac='00:00:00:00:00:08', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='10.0.0.10', mac='00:00:00:00:00:09', defaultRoute=None)
    h10 = net.addHost('h10', cls=Host, ip='10.0.0.11', mac='00:00:00:00:00:10', defaultRoute=None)
    h11 = net.addHost('h11', cls=Host, ip='10.0.0.12', mac='00:00:00:00:00:11', defaultRoute=None)
    h12 = net.addHost('h12', cls=Host, ip='10.0.0.13', mac='00:00:00:00:00:12', defaultRoute=None)
    h13 = net.addHost('h13', cls=Host, ip='10.0.0.14', mac='00:00:00:00:00:13', defaultRoute=None)
    h14 = net.addHost('h14', cls=Host, ip='10.0.0.15', mac='00:00:00:00:00:14', defaultRoute=None)
    h15 = net.addHost('h15', cls=Host, ip='10.0.0.16', mac='00:00:00:00:00:15', defaultRoute=None)
    h16 = net.addHost('h16', cls=Host, ip='10.0.0.17', mac='00:00:00:00:00:16', defaultRoute=None)
    h17 = net.addHost('h17', cls=Host, ip='10.0.0.18', mac='00:00:00:00:00:17', defaultRoute=None)
    h18 = net.addHost('h18', cls=Host, ip='10.0.0.19', mac='00:00:00:00:00:18', defaultRoute=None)
    h19 = net.addHost('h19', cls=Host, ip='10.0.0.20', mac='00:00:00:00:00:19', defaultRoute=None)
    h20 = net.addHost('h20', cls=Host, ip='10.0.0.21', mac='00:00:00:00:00:20', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(h6, s4)
    net.addLink(h7, s4)
    net.addLink(h8, s5)
    net.addLink(h9, s5)
    net.addLink(h1, s6)
    net.addLink(s1, s6)
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s1, s4)
    net.addLink(s1, s5)
    net.addLink(h2, s2)
    net.addLink(h3, s2)
    net.addLink(h4, s3)
    net.addLink(h5, s3)
    net.addLink(h10, s2)
    net.addLink(h11, s3)
    net.addLink(h12, s4)
    net.addLink(h13, s5)
    net.addLink(h14, s6)
    net.addLink(h15, s2)
    net.addLink(h16, s3)
    net.addLink(h17, s4)
    net.addLink(h18, s5)
    net.addLink(h19, s6)
    net.addLink(h20, s2)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s4').start([c0])
    net.get('s6').start([c0])
    net.get('s5').start([c0])
    net.get('s3').start([c0])
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
