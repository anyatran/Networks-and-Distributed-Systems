import socket, sys
# Secret Key 
# 9503ad389fb5789ecfd482306029f499c0cb3b06ad12002b4785d8a497193673
sys.setrecursionlimit(10000)
# GLOBAL
server_address = ('login.ccs.neu.edu', 27993)
# calculates an expression
def calculate_expr(d, s):
    if "STATUS" in d:
        expression = d.split("STATUS ", 1)[1]
        print 'cs3700fall2015 STATUS %s' % expression 
        if expression.split(" ")[1] == '+' or expression.split(" ")[1] == '-' or expression.split(" ")[1] == '/' or expression.split(" ")[1] == '*':
            solution = eval(expression)
            solution_msg = 'cs3700fall2015 %d' % (solution) + '\n'
            print solution_msg
            s.sendall(solution_msg)
            d_new = s.recv(8192)
            calculate_expr(d_new, s)
        else:
            print 'Unknown mathematical expression %s\n' % expression
            s.close()
    elif "BYE" in d:
        print 'cs3700fall2015 BYE %s\n' % d.split("BYE ", 1)[1]
        s.close()
    # other than STATE and BYE messages
    else:                                                              
        print 'Received unknown type of message: %s\n' % d          
        print 'closing socket'                                         
        s.close()

# Initialize the socket
def init_socket(adr):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        print 'connecting to %s port %s' % server_address
        
        try:
            message = 'cs3700fall2015 HELLO 001959524\n'
            print message
            sock.sendall(message)
            data = sock.recv(8192)
            calculate_expr(data, sock)
        except:
            e = sys.exc_info()[0]
            print 'ERROR occured: %s\n' % e
        finally:
            print 'closing socket'
    except socket.error, (value, message):
        print 'Couldnt open socket: ' + message

init_socket(server_address)
