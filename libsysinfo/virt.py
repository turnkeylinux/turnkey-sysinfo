import subprocess


def check_vm():
    out = subprocess.run(
        ["systemd-detect-virt", "-v"], capture_output=True, text=True
    ).stdout.strip()
    if out:
        return out


def check_container():
    out = subprocess.run(
        ["systemd-detect-virt", "-c"], capture_output=True, text=True
    ).stdout.strip()
    if out:
        return out


def is_proxmox():
    out = subprocess.run(
        ["uname", "-r"], capture_output=True, text=True
    ).stdout.strip()
    return out.lower().endswith("-pve")


def format_virt():
    virt = check_vm()
    if not virt:
        virt = check_container()
        if not virt:
            return f"not virtualised"
        if is_proxmox():
            virt += " on Proxmox"

        return virt
    return virt
