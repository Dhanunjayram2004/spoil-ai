from core.registry import tool
from core.dependency import check_command, install_package
import subprocess



@tool(
    "network_info",
    "Get current IP address and network information"
)
def network_info():

    result = subprocess.run(
        "ip addr && echo '---' && ip route",
        shell=True,
        capture_output=True,
        text=True
    )

    return {
        "success": True,
        "stdout": result.stdout,
        "stderr": result.stderr
    }




@tool(
    "get_network_range",
    "Get local network range for scanning"
)
def get_network_range():

    result = subprocess.run(
        "ip route",
        shell=True,
        capture_output=True,
        text=True
    )

    lines = result.stdout.splitlines()

    for line in lines:

        if "proto kernel" in line and "src" in line:

            network = line.split()[0]

            return {
                "success": True,
                "stdout": network,
                "stderr": ""
            }


    return {
        "success": False,
        "stdout": "",
        "stderr": "Network not found"
    }




@tool(
    "network_scan",
    "Scan devices on your local network using nmap",
    requires="nmap"
)
def network_scan(network):


    # Check nmap dependency

    if not check_command("nmap"):

        installed = install_package("nmap")


        if not installed:

            return {
                "success": False,
                "stdout": "",
                "stderr": "nmap installation cancelled"
            }



    print()
    print(f"SPOIL: Scanning network {network}")
    print()


    command = f"nmap -sn {network}"


    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )


    return {
        "success": True,
        "stdout": result.stdout,
        "stderr": result.stderr
    }




@tool(
    "open_ports",
    "Check open ports on a host"
)
def open_ports(target):


    if not check_command("nmap"):

        installed = install_package("nmap")


        if not installed:

            return {
                "success": False,
                "stdout": "",
                "stderr": "nmap installation cancelled"
            }



    command = f"nmap {target}"


    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )


    return {
        "success": True,
        "stdout": result.stdout,
        "stderr": result.stderr
    }
