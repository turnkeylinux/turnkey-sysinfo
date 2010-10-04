import os
import statvfs

def _get_mounts(mounts_file="/proc/mounts"):
    """
    Given a mounts file (e.g., /proc/mounts), generate dicts with the following
    keys:

     - device: The device file which is mounted.
     - mount-point: The path at which the filesystem is mounted.
     - filesystem: The filesystem type.
     - total-space: The capacity of the filesystem in megabytes.
     - free-space: The amount of space available in megabytes.
    """
    for line in open(mounts_file):

        try:
            device, mount_point, filesystem = line.split()[:3]
            mount_point = mount_point.decode("string-escape")
        except ValueError:
            continue

        megabytes = 1024 * 1024
        stats = os.statvfs(mount_point)
        block_size = stats[statvfs.F_BSIZE]
        total_space = (stats[statvfs.F_BLOCKS] * block_size) / megabytes
        free_space = (stats[statvfs.F_BFREE] * block_size) / megabytes

        yield { "device": device, 
                "mount-point": mount_point,
                "filesystem": filesystem, 
                "total-space": int(total_space),
                "free-space": int(free_space) }

def _get_filesystem_for_path(path, mounts_file="/proc/mounts"):
    candidate = None

    path = os.path.realpath(path)
    path_segments = path.split("/")

    for info in _get_mounts(mounts_file):
        if not path.startswith(info["mount-point"]):
            continue

        mount_segments = info["mount-point"].split("/")

        if ((not candidate)
            or path_segments[:len(mount_segments)] == mount_segments):
            candidate = info

    return candidate

def _format_megabytes(megabytes):
    if megabytes >= 1024*1024:
        return "%.2fTB" % (megabytes/(1024*1024.0))
    elif megabytes >= 1024:
        return "%.2fGB" % (megabytes/1024.0)
    else:
        return "%dMB" % (megabytes)

def _format_used(info):
    total = info["total-space"]
    used = total - info["free-space"]
    return "%0.1f%% of %s" % ((used / float(total)) * 100, _format_megabytes(total))

def usage(path):
    return _format_used(_get_filesystem_for_path(path))
