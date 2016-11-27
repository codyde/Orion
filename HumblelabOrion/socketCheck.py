import socket


def check_server(address, port):
    # Create a TCP socket
    s = socket.socket()
    # print("Attempting to connect to %s on port %s" % (address, port))
    try:
        s.connect((address, port))
        # print("Connected to %s on port %s" % (address, port))
        return True
    except socket.error as e:
        # print("Connection to %s on port %s failed: %s" % (address, port, e))
        return False
