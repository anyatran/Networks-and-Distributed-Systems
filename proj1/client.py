import socket
import sys

# Server address to connect to
server_address = ('login.ccs.neu.edu', 27993)
secret_key = '9e2677f4533cad7f9bafea36b10789e';

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    print 'connecting to %s port %s' % server_address

    try:
   
        # Sending first type of message
        message = 'cs3700fall2015 HELLO 001910132\n'
        print message 
        sock.sendall(message)

        # Receive first STATUS message
        data = sock.recv(50)
        print data

        while "cs3700fall2015 STATUS" in data:
            # Get mathematical expression, for example: 3 + 4
            expression = data.split("STATUS ", 1)[1]
            # Evaluate mathematical expression
            solution = eval(expression)
            # Check if this expression containes one of four allowed mathematical operations
            if expression.split(" ")[1] == '+' or expression.split(" ")[1] == '-' or expression.split(" ")[1] == '/' or expression.split(" ")[1] == '*':
                solution_message = 'cs3700fall2015 %d' % (solution) + '\n' 
                print solution_message 
                # Send solution
                sock.sendall(solution_message)
                # Receive new STATUS message
                data = sock.recv(50)
            else:
                print 'Unknown mathematical expression: "%s"' % expression
                break

        # If received data does not contain STATUS message anymore check if it is a BYE message
        if "cs3700fall2015 BYE" in data:
            print 'Received BYE message with secret key "%s"' % data.split("BYE ", 1)[1]
        else:
            print 'Received unknown type of message: "%s"' % data
            print 'closing socket'
            sock.close()

    except:
        print "ERROR occured"
    finally:
        print 'closing socket'
        sock.close()

except socket.error, (value, message):    
    print "Could not open socket: " + message



    #division by zero?




    