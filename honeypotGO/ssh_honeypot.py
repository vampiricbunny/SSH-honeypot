# Libraries
import logging
from logging.handlers import RotatingFileHandler
import paramiko
import socket
import threading
import paramiko.transport
# Constants
logging_format = logging.Formatter('%(message)s')
SSH_BANNER = 'SSH-2.0-MySSHServer_1.0'


#host_key = 'server.key'
host_key = paramiko.RSAKey(filename='server.key')
# Loggers & Logging Files
funeel_logger = logging.getLogger('FuneelLogger')
funeel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler('audits.log', maxBytes=2000, backupCount=5)
funnel_handler.setFormatter(logging_format)
funeel_logger.addHandler(funnel_handler)

creds_logger = logging.getLogger('CredsLogger')
creds_logger.setLevel(logging.INFO)
creds_handler = RotatingFileHandler('cmd_audits.log', maxBytes=2000, backupCount=5)
creds_handler.setFormatter(logging_format)
creds_logger.addHandler(creds_handler)


# Emulated Shell
def emulated_shell(channel, client_ip):
    channel.send(b'root@kali$ ')
    command = b""
    while True:
        char = channel.recv(1)
        channel.send(char)
        if not char:
            channel.close()

        command += char

        if char in [b'\r', b'\n']:
            if command.strip() == b'exit':
                response = b'\nGoodbye!\n'
                creds_logger.info(f"Command: {command.strip().decode('utf-8')} executed by {client_ip}")
                channel.close()
            elif command.strip() == b'pwd':
                response = b'\n/home/ssh_honeypot\n\r\n'
                creds_logger.info(f'Command: {command.strip().decode('utf-8')}' + ' executed by '+ f'{client_ip}')
            elif command.strip() == b'whoami':
                response = b'\nroot\n\r\n'
                creds_logger.info(f"Command: {command.strip().decode('utf-8')} executed by {client_ip}")
            elif command.strip() == b'ls':
                response = b'\nbin\n\rboot\n\rdev\r\netc\r\nhome\r\nlib\r\nlib64\r\nmedia\r\nmnt\r\nopt\r\nproc\r\nroot\r\nrun\r\nsbin\r\nsrv\r\nsys\r\ntmp\r\nusr\r\nvar\n' + b'\r\n'
                creds_logger.info(f"Command: {command.strip().decode('utf-8')} executed by {client_ip}")
            elif command.strip() == b'cat':
                response = b'\nNice try...\n\r\n'
                creds_logger.info(f"Command: {command.strip().decode('utf-8')} executed by {client_ip}")
            else:
                response = b'\n' + bytes(command.strip()) + b'\r\n'   

            channel.send(response)
            channel.send(b"root@kali$ ")
            command = b""


# SSH Server + Sockets
class Server(paramiko.ServerInterface):
     
    def __init__(self, client_ip, input_username = None, input_password = None):
        self.event = threading.Event()
        self.client_ip = client_ip
        self.input_username = input_username
        self.input_password = input_password
    
    def check_channel_request(self, kind: str, chanid: int) -> int:
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED

    def get_allowed_auth(self):
        return 'password'                    

    def check_auth_password(self, username, password):
        funeel_logger.info(f'Client IP: {self.client_ip} attepted connection with ' + f'username: {username}, ' + f'password: {password}')
        creds_logger.info(f'{self.client_ip}, {username}, {password}')
        if self.input_username is not None and self.input_password is not None:
            if username == self.input_username and password == self.input_password:
                return paramiko.AUTH_SUCCESSFUL
            else:
                return paramiko.AUTH_FAILED
        else:
            return paramiko.AUTH_SUCCESSFUL
            
    def check_channel_shell_request(self, channel):
        self.event.set()
        return True
    
    # def for setting pseudoterminal
    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True
    # def for direct command execute 'ssh root@pass ls -la'
    def check_channel_exec_request(self, channel, command):
        command = str(command)
        return True

def client_handle(client, addr, username, password):
    client_ip = addr[0]
    print(f"{client_ip} has connected to the server.")

    try:
        
        transport = paramiko.Transport(client)
        transport.local_version = SSH_BANNER
        server = Server(client_ip = client_ip, input_username = username, input_password = password)

        transport.add_server_key(host_key)
        
        transport.start_server(server = server)

        channel = transport.accept(100)
        if channel is None:
            print('No channel was opened.')
        
        standard_banner = "Welcom to Ubuntu 22.04 LTS (GNU/Linux 5.4.0-80-generic x86_64)\r\n\r\n"

        channel.send(standard_banner)
        emulated_shell(channel, client_ip = client_ip)

    except Exception as error:
        print(f"An error occurred 1: {error}")
    finally:
        try:
            transport.close()
        except Exception as error:
            print(f"An error occurred 2: {error}")
        client.close()


# Provision SSH-based Honeypot
def honeypot(address, port, username, password):
    
    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socks.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socks.bind((address, port))

    socks.listen(100)
    print(f"SSH server listening on {address}:{port}")

    while True:
        try:
            client, addr = socks.accept()
            ssh_honeypot_thread = threading.Thread(target=client_handle, args=(client, addr, username, password))   
            ssh_honeypot_thread.start()

        except Exception as error:
            print(f"An error occurred 3: {error}")

honeypot('127.0.0.1', 2222, username = None, password = None)