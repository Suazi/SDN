#!/usr/bin/python

from mininet.topo import Topo

class DatacenterBasicTopo( Topo ):
	"Datacenter topo 4 hosts per rack, 4 racks and root switch"
	def build(self):
		self.racks = []
		rootSwitch = self.addSwitch('s1')
		for i in range(1, 5):
			rack = self.buildRack(i)
			self.racks.append(rack)
			for switch in rack:
				self.addLink(rootSwitch, switch)

	def buildRack(self, loc):
		dpid = (loc * 16  ) + 1
		switch = self.addSwitch('s1r%s' % loc, dpid='%x' % dpid)

		for n in range(1, 5):
			host = self.addHost('h%sr%s' % (n, loc))
			self.addLink(switch, host)

		return [switch]

topos = {'dcbasic': DatacenterBasicTopo}
