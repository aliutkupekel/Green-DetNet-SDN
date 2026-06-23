#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info

def create_wan_slice():
    setLogLevel('info')
    net = Mininet(controller=RemoteController, switch=OVSKernelSwitch, link=TCLink)
    
    info("*** Adding SDN Controller (Control Plane) ***\n")
    c0 = net.addController('c0', port=6653)
    
    info("*** Adding TSN-enabled Switches ***\n")
    s1 = net.addSwitch('s1') # Ingress Switch
    s2 = net.addSwitch('s2') # Core Switch 1 (Primary Path)
    s3 = net.addSwitch('s3') # Core Switch 2 (Backup Path - Can Sleep)
    s4 = net.addSwitch('s4') # Egress Switch
    
    info("*** Adding Cyber-Physical System Hosts ***\n")
    h1 = net.addHost('h1', ip='10.0.0.1')
    h2 = net.addHost('h2', ip='10.0.0.2')
    
    info("*** Creating Deterministic Links (Bandwidth & Latency bounded) ***\n")
    net.addLink(h1, s1, bw=1000, delay='1ms')
    net.addLink(s1, s2, bw=1000, delay='5ms') # Primary Path
    net.addLink(s2, s4, bw=1000, delay='5ms')
    net.addLink(s1, s3, bw=1000, delay='6ms') # Redundant Backup Path
    net.addLink(s3, s4, bw=1000, delay='6ms')
    net.addLink(s4, h2, bw=1000, delay='1ms')
    
    info("*** Starting Green-DetNet Emulation ***\n")
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    create_wan_slice()