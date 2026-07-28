import shutil

SUDO_COMMANDS = {
    "apt",
    "apt-get",
    "systemctl",
    "mount",
    "umount",
    "fdisk",
    "iptables",
    "ufw",
    "tcpdump",
    "airmon-ng",
    "aireplay-ng",
    "airodump-ng",
    "aircrack-ng",
}


def needs_sudo(command):

    exe = command.split()[0]

    return exe in SUDO_COMMANDS
