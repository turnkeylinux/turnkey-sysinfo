#!/usr/bin/python
# 
# Copyright (c) 2010 Liraz Siri <liraz@turnkeylinux.org>
# 
# This file is part of turnkey-sysinfo
# 
# turnkey-sysinfo is open source software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
# 
import os
import re

import disk
from memstats import MemoryStats

import netinfo 

NIC_BLACKLIST = ('lo')

def get_nics():
    nics = []

    for ifname in netinfo.get_ifnames():
        if ifname in NIC_BLACKLIST:
            continue

        nic = netinfo.InterfaceInfo(ifname)
        if nic.is_up and nic.address:
            nics.append((ifname, nic.address))

    return nics

def get_loadavg():
    return os.getloadavg()[0]

def get_pids():
    return [ int(dentry) for dentry in os.listdir("/proc") 
             if re.match(r'\d+$', dentry) ]

def main():
    print "System load: %.2f" % get_loadavg()
    print "Processes: %d" % len(get_pids())
    print "Usage of /: "  + disk.usage("/")

    memstats = MemoryStats()
    print "Memory usage: %d%%" % memstats.used_memory_percentage
    print "Swap usage: %d%%" % memstats.used_swap_percentage

    for nic, address in get_nics():
        print "IP address for %s: %s" % (nic, address)
    
if __name__=="__main__":
    main()

