from mininet.topo import Topo
from mininet.util import irange
from collections import defaultdict


class SpineLeaf(Topo):
    """Spine - Leaf data center topology"""

    def build(self, num_spine_sw=4, num_racks=8, hosts_per_rack=4, sw_per_rack=1):
        "Build network from racks and spine switches"
        spine_switches = []
        leaf_switches = []
        self.racks = defaultdict(list)

        # Create spine switches
        for n in irange(1, num_spine_sw):
            spine_sw = self.addSwitch('spine%s' % n)
            spine_switches.append(spine_sw)

        # Create racks
        for n in irange(1, num_racks):
            # build_rack() returns list of leaf switches
            leaf_switches.append(self.build_rack(n, hosts_per_rack, sw_per_rack))
            #_diff_ip makes each rack in different subnet
            #leaf_switches.append(self.build_rack_diff_ip(n, hosts_per_rack, sw_per_rack))

        # Create links between spine and leaf (ToR) switches
        # print spine_switches
        # print leaf_switches
        for spine in spine_switches:
            for leaf in leaf_switches:
                self.addLink(spine, leaf)

    def build_rack(self, rack_nr, hosts_per_rack, sw_per_rack):
        "Build rack of hosts with ToR switch"
        switches = []
        hosts = []

        # Create ToR switches
        for n in irange(1, sw_per_rack):
            # Make sure each switch gets unique dpid
            # for easy log checking
            dpid = (rack_nr * 16) + 1
            switch = self.addSwitch('s%sr%s' % (n, rack_nr), dpid='%x' % dpid)
            switches.append(switch)

        # Create hosts in rack
        for n in irange(1, hosts_per_rack):
            host = self.addHost('h%sr%s' % (n, rack_nr))
            hosts.append(host)
            self.racks[rack_nr].append(host)

        # Create links between ToR switches and hosts
        for switch in switches:
            for host in hosts:
                self.addLink(switch, host)

        # Return ToR switches in order to connect them to spine
        return switches[0]

    def build_rack_diff_ip(self, rack_nr, hosts_per_rack, sw_per_rack):
        "Build rack of hosts with ToR switch"
        switches = []
        hosts = []

        # Create ToR switches
        for n in irange(1, sw_per_rack):
            # Make sure each switch gets unique dpid
            # for easy log checking
            dpid = (rack_nr * 16) + 1
            switch = self.addSwitch('s%sr%s' % (n, rack_nr), dpid='%x' % dpid)
            switches.append(switch)

        # Create hosts in rack
        for n in irange(1, hosts_per_rack):
            host = self.addHost('h%sr%s' % (n, rack_nr), ip='10.0.%d.%d/24' % (rack_nr, 100 + n), 
                                defaultRoute='via 10.0.%d.1' % rack_nr)
            hosts.append(host)
            self.racks[rack_nr].append(host)

        # Create links between ToR switches and hosts
        for switch in switches:
            for host in hosts:
                self.addLink(switch, host)

        # Return ToR switches in order to connect them to spine
        return switches[0]

    def set_hosts_ip(self):
        for rack in self.racks:
            for host in self.racks[rack]:
                ip = 101
                self.get(host).setIP('10.0.%s.%d' % (rack, ip))
                ip += 1




# Allows the file to be imported using 'mn --custom <filename> --topo toponame'
topos = {
    'spine_leaf': SpineLeaf
}

