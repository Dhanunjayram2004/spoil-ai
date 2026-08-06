from core.registry import tool
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
    "Check open ports on a host",
    requires="nmap"
)
def open_ports(target):
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

@tool(
    "wifi_security",
    "Show the security protocol of the connected Wi-Fi",
    requires="nmcli"
)
def wifi_security():
    # 1. Run nmcli natively to capture exact OS output and errors
    result = subprocess.run(
        ["nmcli", "-t", "-f", "ACTIVE,SSID,SECURITY", "dev", "wifi"],
        capture_output=True,
        text=True
    )

    # 2. If OS throws an error (e.g., no hardware), return OS error dynamically
    if result.returncode != 0:
        return {
            "success": False,
            "stdout": "",
            "stderr": result.stderr.strip() or result.stdout.strip()
        }

    # 3. Filter for active connections in Python instead of using grep
    output = result.stdout.strip()
    active_lines = [line for line in output.splitlines() if line.startswith("yes:")]

    if active_lines:
        return {
            "success": True,
            "stdout": "\n".join(active_lines).replace("yes:", "Active Wi-Fi: "),
            "stderr": ""
        }

    # 4. No active Wi-Fi found. Instead of hardcoding text, let the OS explain its state
    fallback = subprocess.run(
        ["nmcli", "general", "status"],
        capture_output=True,
        text=True
    )
    
    return {
        "success": True,
        "stdout": fallback.stdout.strip(),
        "stderr": fallback.stderr.strip()
    }
