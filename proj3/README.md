<b> REQUIREMENTS\: </b><br/>
    - command syntax\: ./3700send \<recv_host\>\:\<recv_port\> <br/>
    - The sender must accept data from STDIN, sending data until EOF is reached<br/>
    - The sender and receiver must work together to transmit the data reliably<br/>
    - The receiver must print out the received data to STDOUT in order and without errors<br/>
    - The sender and receiver must print out specified debugging messages to STDERR<br/>
    - Your sender and receiver must gracefully exit<br/>
    - Your code must be able to transfer a file with any number of packets dropped, damaged, duplicated, and delayed, and under a variety of different available bandwidths and link latencies<br/>
    - Your sending program must be named 3700send and your receiving program must be named 3700recv<br/>
