# Copyright (c) 2010 Liraz Siri <liraz@turnkeylinux.org>
#
# This file is part of turnkey-sysinfo.
#
# turnkey-sysinfo is open source software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.

import re
from subprocess import run, PIPE
from os.path import join
from sys import stdin


def _parse_turnkey_release(version):
    m = re.match(r'turnkey-.*?-(\d.*?)-[^\d]', version)
    if m:
        return m.group(1)


def get_turnkey_release(rootfs='/'):
    """Return release_version. On error, returns None"""
    turnkey_version = get_turnkey_version(rootfs=rootfs)
    if turnkey_version:
        return _parse_turnkey_release(turnkey_version)


def get_turnkey_version(rootfs='/'):
    """Return turnkey_version. On error, returns None"""
    try:
        with open(join(rootfs, "etc/turnkey_version"), 'r') as fob:
            return fob.read().strip()
    except IOError:
        pass


def fmt_base_distribution(encoding):
    """Return a formatted distribution string:
        e.g., Debian 10/Buster"""

    process = run(["lsb_release", "-ircd"], stdout=PIPE)
    if process.returncode != 0:
        return

    d = dict([line.split(':\t')
              for line in process.stdout.decode(encoding).splitlines()])

    codename = d['Codename'].capitalize()
    basedist = "{} {}/{}".format(d['Distributor ID'],
                                 d['Release'],
                                 d['Codename'].capitalize())
    return basedist


def fmt_sysversion(encoding=stdin.encoding):
    version_parts = []
    release = get_turnkey_release()
    if release:
        version_parts.append("TurnKey GNU/Linux {}".format(release))

    basedist = fmt_base_distribution(encoding)
    if basedist:
        version_parts.append(basedist)

    if len(version_parts) == 2:
        version = '{} ({})'.format(version_parts[0], version_parts[1])
    elif len(version_parts) == 1:
        version = version_parts[0]
    else:
        version = "Unknown"
    return version
