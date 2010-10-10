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

from datetime import datetime
import netinfo 

import commands

NIC_BLACKLIST = ('lo')

def get_nics():
    nics = []

    for ifname in netinfo.get_ifnames():
        if ifname in NIC_BLACKLIST:
            continue

        nic = netinfo.InterfaceInfo(ifname)
        if nic.is_up and nic.address:
            nics.append((ifname, nic.address))

    nics.sort(lambda a,b: cmp(a[0], b[0]))
    return nics

def get_loadavg():
    return os.getloadavg()[0]

def get_pids():
    return [ int(dentry) for dentry in os.listdir("/proc") 
             if re.match(r'\d+$', dentry) ]

def main():
    system_load = "System load:  %.2f" % get_loadavg()

    processes = "Processes:    %d" % len(get_pids())
    disk_usage = "Usage of /:   "  + disk.usage("/")

    memstats = MemoryStats()

    memory_usage = "Memory usage:  %d%%" % memstats.used_memory_percentage
    swap_usage = "Swap usage:    %d%%" % memstats.used_swap_percentage

    rows = []
    rows.append((system_load, memory_usage))
    rows.append((processes, swap_usage))

    nics = [ "IP address for %s:  %s" % (nic, address)
             for nic, address in get_nics() ]

    column = [disk_usage]
    if nics:
        column.append(nics[0])
    rows.append(column)
    for nic in nics[1:]:
        rows.append(('', nic))

    print "System information (as of %s)" % datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    print
    max_col = max([ len(row[0]) for row in rows ])
    tpl = "  %%-%ds   %%s" % max_col
    for row in rows:
        print tpl % (row[0], row[1])

    if os.geteuid() == 0:
        error, output = commands.getstatusoutput("tklbam-status")
        error_nosuchcommand = (os.WEXITSTATUS(error) == 127)

        if not error_nosuchcommand:
            print
            print output,

if __name__=="__main__":
    main()
