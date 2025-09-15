import subprocess


def check_vm() -> str | None:
    detected_vm = subprocess.run(
        ["systemd-detect-virt", "-v"], capture_output=True, text=True
    ).stdout.strip()
    if detected_vm:
        return detected_vm
    return None


def check_container() -> str | None:
    detected_ct = subprocess.run(
        ["systemd-detect-virt", "-c"], capture_output=True, text=True
    ).stdout.strip()
    if detected_ct:
        return detected_ct
    return None


def is_proxmox() -> bool:
    kernel_v = subprocess.run(
        ["uname", "-r"], capture_output=True, text=True
    ).stdout.strip()
    return kernel_v.lower().endswith("-pve")


def format_virt() -> str:
    virt = check_vm()
    if not virt:
        virt = check_container()
        if not virt:
            return "not virtualised"
        if is_proxmox():
            virt += " on Proxmox"

        return virt
    return virt
