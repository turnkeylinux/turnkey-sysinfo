import os
from collections.abc import Iterator


def _get_mounts(
    mounts_file: str = "/proc/mounts"
) -> Iterator[dict[str, str | int]]:
    """
    Given a mounts file (e.g., /proc/mounts), generate dicts with the following
    keys:

     - device (str): The device file which is mounted.
     - mount-point (str): The path at which the filesystem is mounted.
     - filesystem (str): The filesystem type.
     - total-space (int): The capacity of the filesystem in megabytes.
     - free-space (int): The amount of space available in megabytes.
    """
    for line in open(mounts_file):
        try:
            device, mount_point, filesystem = line.split()[:3]
            # the following line could cause issues with unicode escapes
            mount_point = bytes(mount_point, "utf-8").decode("unicode-escape")
        except ValueError:
            continue

        megabytes = 1024 * 1024
        stats = os.statvfs(mount_point)
        block_size = stats.f_bsize
        total_space = (stats.f_blocks * block_size) / megabytes
        free_space = (stats.f_bfree * block_size) / megabytes

        yield {
            "device": device,
            "mount-point": mount_point,
            "filesystem": filesystem,
            "total-space": int(total_space),
            "free-space": int(free_space),
        }


def _get_filesystem_for_path(
    path: str, mounts_file: str = "/proc/mounts"
) -> dict[str, str | int] | None:
    candidate = None

    path = os.path.realpath(path)
    path_segments = path.split("/")

    for info in _get_mounts(mounts_file):
        # info["mount-point"] is a str
        if not path.startswith(str(info["mount-point"])):
            continue

        mount_segments = str(info["mount-point"]).split("/")

        if (not candidate) or path_segments[
            : len(mount_segments)
        ] == mount_segments:
            candidate = info

    return candidate


def _format_megabytes(megabytes: int) -> str:
    if megabytes >= 1024 * 1024:
        return f"{megabytes / (1024 * 1024.0):.2f}TB"
    elif megabytes >= 1024:
        return f"{megabytes / 1024.0:.2f}GB"
    else:
        return f"{megabytes}MB"


def _format_used(info: dict[str, str | int] | None) -> str | None:
    if not info:
        return None
    # info["total-space"] is an int
    total = int(info["total-space"])
    used = total - int(info["free-space"])
    return f"{used / float(total) * 100:.1f}% of {_format_megabytes(total)}"


def usage(path: str) -> str | None:
    return _format_used(_get_filesystem_for_path(path))
