# SSH-honeypot
a simple ssh honey pot to see how people attack things.


# SSH Honeypot for Credential Logging and Attack Analysis
This is not ground breaking. Just a how to capture cool stuff.:

This project is a fully functional SSH honeypot designed to emulate a real SSH server while capturing login attempts and command executions from attackers. 
Honeypot logs all connection attempts, including credentials used, executed commands, and session interactions. This can be used for security research, attack analysis, and proactive defense strategies.

### Features:
- **SSH Emulation:** Mimics / fakes a real SSH server with a standard Linux shell prompt.
- **Credential Logging:** Captures usernames and passwords used by attackers.
- **Command Logging:** Records all executed commands for forensic analysis.
- **Rotating Log Files:** Maintains a structured logging with `RotatingFileHandler`.
- **Threaded Handling:** Supports multiple simultaneous connections.
- **Fake File System Structure:** Provides basic responses for common commands like `pwd`, `whoami`, and `ls`.
- **Custom SSH Banner:** Make the honeypot as a legitimate server or make it fake it till it makes it.

## Installation & Setup
### Prerequisites:
- Python 3.x
- `paramiko` library

### Installation:
1. Clone the repository:
   ```sh
   git clone https://github.com/vampiricbunny/SSH-honeypot
   cd ssh-honeypot
   ```
2. Install dependencies:
   ```sh
   pip install paramiko
   ```
3. Generate an SSH host key if not available:
   ```sh
   ssh-keygen -t rsa -b 2048 -f server.key
   ```
4. Run the honeypot:
   ```sh
   python ssh_honeypot.py
   ```

## Usage
The honeypot listens on a specified IP/port, capturing ALL SSH login attempts.
- To change the listening address and port, modify:
  ```python
  honeypot('0.0.0.0', 2222, username=None, password=None)
  ```
  This will listen on all network interfaces on port 2222.

- Logs are stored in `audits.log` and `cmd_audits.log`:
  - `audits.log`: Stores authentication attempts (IP, username, password)
  - `cmd_audits.log`: Stores executed commands and session activity

## Example output from attacks:
```
Client IP: 192.168.1.10 attempted connection with username: admin, password: password123
Command: ls executed by 192.168.1.10
Command: whoami executed by 192.168.1.10
```

## Potential Use Cases
- **Threat Intelligence**: Monitor brute-force SSH attacks and analyze attacker behavior.
- **Security Research**: Collect real-world credential data and attack patterns.
- **Enterprise Security**: Deploy as a deception technology to track and prevent intrusions.

## Future Enhancements
- Integration with a central logging server for real-time monitoring.
- Web-based dashboard for visualizing login attempts and commands.
- Support for more realistic command emulation to deceive attackers.
- Alert system to notify administrators of suspicious activity.

## Recruiter-specific Notes
This project demonstrates expertise in:
- Network security and honeypot deployment
- SSH security and authentication mechanisms
- Python programming (multithreading, logging, and socket programming)
- Cyber threat intelligence and forensic analysis

If you are a recruiter or hiring manager, this project showcases my ability to design and deploy security tools, analyze attacks, and improve defensive strategies.  This is just something I put together to show that I’m capable and that I truly earned my certifications.
