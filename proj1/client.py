import socket
import sys
import parser

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('login.ccs.neu.edu', 27993)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
   
    # Send data
    message = 'cs3700fall2015 HELLO 001910132\n'
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(50)
        amount_received += len(data)
        print >>sys.stderr, 'received "%s"' % data
        while "STATUS" in data:
        	solution = eval(data.split("STATUS ", 1)[1])
        	solution_message = 'cs3700fall2015 %d' % solution + '\n' #'cs3700fall2015 52' + str(solution) + '\n'
        	print >>sys.stderr, 'sending solution "%s"' % solution_message
        	data = sock.sendall(solution_message)
        	print >>sys.stderr, 'equation %s' % solution
        	print >>sys.stderr, 'new data %s' % data

        print >>sys.stderr, 'Did not get status message "%s"' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()