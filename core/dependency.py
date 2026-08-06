import shutil
import subprocess
from core.package_map import PACKAGE_MAP

def check_command(command):
    """
    Check if a Linux command exists.
    Example:
    nmap, git, tcpdump
    """
    return shutil.which(command) is not None

def install_package(command_name):
    # Get actual apt package name from map, or fallback to command name
    apt_package = PACKAGE_MAP.get(command_name, command_name)

    print()
    print(f"SPOIL needs '{command_name}' (apt package: {apt_package})")
    print()
    print("Install command:")
    print(f"sudo apt install {apt_package} -y")
    print()

    answer = input("Install now? (y/n): ").strip().lower()

    if answer not in ["y", "yes"]:
        print("Installation cancelled.")
        return False

    print()
    print(f"Installing {apt_package}...")
    print()

    try:
        result = subprocess.run(
            ["sudo", "apt", "install", apt_package, "-y"]
        )

        if result.returncode == 0:
            print()
            print(f"{apt_package} installed successfully.")
            return True
        else:
            print()
            print(f"Failed installing {apt_package}.")
            return False

    except KeyboardInterrupt:
        print("\nInstallation interrupted.")
        return False
