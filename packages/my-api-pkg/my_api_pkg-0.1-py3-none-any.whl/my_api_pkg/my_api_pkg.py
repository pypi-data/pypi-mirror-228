import ipaddress
import socketserver
import ssl
import socket
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler



class PP_IP_MODULE:
    """
    IPv4 address_generator Module
    ===================

    This PP_IP_MODULE provides functions for generating IPv4 addresses and ranges.

    """
    def __init__(self,cidr_network):
        self.cidr_network = cidr_network

    def print_input(self):
        print(self.cidr_network)
    """
    Generate a list of IP addresses from an IP range.

    :param ip_range: The IP range in the form 'x.x.x.x/y'.
    :type ip_range: str
    :return: List of generated IP addresses.
    :rtype: list
    """
    def generate_ip(self):
        net_ipv4_address = ipaddress.IPv4Network(self.cidr_network)
        ip_addresses = [str(ip) for ip in net_ipv4_address.hosts()]
        #print(ip_addresses)
        return ip_addresses




class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    Custom TCP handler class for socketserver.
    
    This class inherits from socketserver.BaseRequestHandler and provides
    the implementation for handling client connections and communication.
    When a client connects, the handle method is called, and it continues
    to receive and send data until the client disconnects.
    """
    def handle(self):
        """
        Handle method to process client requests.
        
        This method is called when a client connects to the server. It receives
        data from the client, processes it, and sends a response back. The client's
        address is displayed along with the received and sent messages.
        """
        print(f"Connected from {self.client_address}")
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Received from {self.client_address}: {message}")
            response = f"Received: {message}"
            self.request.sendall(response.encode('utf-8'))
        print(f"Connection from {self.client_address} closed")


class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    Custom UDP handler class for socketserver.
    
    This class inherits from socketserver.BaseRequestHandler and provides
    the implementation for handling UDP client requests. It receives data
    from clients, processes it, and sends a response back to the client.
    """
    def handle(self):
        """
        Handle method to process UDP client requests.
        
        This method is called when a UDP client sends a message to the server.
        It receives data and the socket from the request, decodes the message,
        constructs a response, and sends the response back to the client.
        """
        data, socket = self.request
        message = data.decode('utf-8')
        print(f"Received from {self.client_address}: {message}")
        response = f"Received: {message}"
        socket.sendto(response.encode('utf-8'), self.client_address)




class MyXMLRPCServer:
    """
    A simple XML-RPC server implementation in Python.
    
    This class sets up an XML-RPC server that listens on a specified host and port.
    It registers the methods of the current instance to be remotely accessible through XML-RPC.
    The methods registered can perform addition, multiplication, and division operations.
    The server runs indefinitely until manually shut down.
    
    Attributes:
        host (str): The hostname or IP address on which the server listens.
        port (int): The port number on which the server listens.
        server (SimpleXMLRPCServer): The XML-RPC server instance.
    """
    def __init__(self, host, port):
        """
        Initialize the XML-RPC server.
        
        Args:
            host (str): The hostname or IP address on which the server listens.
            port (int): The port number on which the server listens.
        """
        self.server = SimpleXMLRPCServer((host, port))
        self.server.register_instance(self)
        print(f"Server listening on {host}:{port}")

    def add(self, x, y):
        """
        Perform addition of two numbers.
        
        Args:
            x (int): The first number.
            y (int): The second number.
            
        Returns:
            int: The sum of x and y.
        """
        return x + y

    def multiply(self, x, y):
        """
        Perform multiplication of two numbers.
        
        Args:
            x (int): The first number.
            y (int): The second number.
            
        Returns:
            int: The product of x and y.
        """
        return x * y

    def divide(self, x, y):
        """
        Perform division of two numbers.
        
        Args:
            x (int): The numerator.
            y (int): The denominator.
            
        Returns:
            float or str: The result of x divided by y, or an error message if y is zero.
        """
        if y != 0:
            return x / y
        else:
            return "Error: Cannot divide by zero"

    def run(self):
        """
        Start serving XML-RPC requests.
        This method starts the server and listens for incoming XML-RPC requests indefinitely.
        """
        self.server.serve_forever()



class SecureSocketServer:
    """
    A class for creating a secure SSL socket server.

    Attributes:
        host (str): The hostname or IP address on which the server will listen.
        port (int): The port number on which the server will listen.
        certfile (str): Path to the server's certificate file.
        keyfile (str): Path to the server's private key file.
        password (str): Password for unlocking the private key (if encrypted).
    """
    def __init__(self, host, port, certfile, keyfile,password):
        """
        Initialize the SecureSocketServer instance.

        Args:
            host (str): The hostname or IP address on which the server will listen.
            port (int): The port number on which the server will listen.
            certfile (str): Path to the server's certificate file.
            keyfile (str): Path to the server's private key file.
            password (str): Password for unlocking the private key (if encrypted).
        """
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile
        self.password = password

    def start(self):
        """
        Start the secure SSL socket server.

        Creates a server socket, sets up SSL context with the provided certificate
        and private key, and starts listening for incoming connections.
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)

        #context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile, password=self.password)

        secure_server_socket = context.wrap_socket(server_socket, server_side=True)

        print(f"SSL Server is listening on {self.host}:{self.port}")

        while True:
            connection, address = secure_server_socket.accept()
            self.handle_client(connection, address)

    def handle_client(self, connection, address):
        """
        Handle an incoming client connection.

        Args:
            connection (socket): The socket representing the client connection.
            address (tuple): The client's IP address and port number.
        """
        data = connection.recv(1024)
        print(f"Received from {address}: {data.decode()}")
        connection.send(b"Hi! This is the response from SSL Server")
        connection.close()
