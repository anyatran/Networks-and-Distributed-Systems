Project 3: Simple Transport Protocol

Higl-level approach

    We decided that for our project we will implement TCP Reno

    Sender

        Sender has the following fields:
            data = ""               - all data that was read from stdin
            cong_window = 1         - congestion window, initially 1
            last_byte_sent = 0      - last byte sent, increments when it was acked
            sent_data = {}          - a dictionary of sent data of the following format: {<sequence_number>: {"sent": <Boolean>, "sent_time": <Double>, "timeout": <Double>}}
            acked_data = {}         - a dictionary of acked data of the following format: {<sequence_number>: <Boolean>}
            RTT = 0.5               - round trip time, half a second initially
            timers = {}             - a dictionary of timers for each sequence number of the following format: {<sequence_number>: <Timer>}
            ssthresh = 50           - slow start threshold, initially 50
            dups_ack_count = {}     - a dictinary of duplicate acks of the following format: {<sequence_number>: <integer>}
            additive_increase = 0   - additive increase float number

        Sender has the following two main functions:
                ## Process acks
            process_ack(self, data)

                ## Sends a packet to the receiver
            send(self)

        Main purpose for sender is to send data and receive acks. 

        When sending packets we first get effective window, which is 
        a range of sequence numbers starting from the last byte that was sent and acked and ending on that byte plus congestion
        window value. That range might include already sent packets, but we check for it before transmitting them. Next we transmit packets in that effective window. Each packet consist of header and data. Header is 20 bytes and includes sequence number, flags (ack, eof), checksum. We store sent packet's sequence number, sent time in sent_data field. We also start a timer for each sent packet. 

        When sender received an ack, we calculate RTT, cancel timeout, check if that data has a duplicate ack, which means that receiver is missing some data. If ack was received for the packet that was last sent, that we increment last_byte_sent variable. Here we also calculate congestion window and marked sequence number as acked in acked_data

        To handle timeouts we have function on_expired_timeout that calculates congeston window and retransmits packet
        To hangle three duplicate acks we have function on_3_dup_acks that calculates congeston window and retransmits packet

        We also have some helper function to decode data, digest data

    Receiver

        Receiver has the following fields
            self.next_byte_expected = 0     - next byte expected that was received yet
            self.buffered_segments = {}     - a dictionary of buffered segments of the following format: {<sequence_number>: {"buffered": <Boolean>, "data": String, "eof": <Boolean>}}
            self.addr = 0                   - address

        Receiver has the following two main functions:
                ## Processes packet
            process_data(self, packet)

                ## Send ACK message to the sender with sequence_number encoded in the specified format
            send_ack(self, sequence_number)

        Main purpose of the receiver is to receive data, print ordered and valid data, and send acks

        When getting data, receiver first checks if this packet is valid, if it is not it ignores it. If it is valid it adds it to buffered_segments, and checks it's order. Received is done when it gets eof packet and if he received all other segments, then he sends an ack to sender with next_byte_expected value of -1. This is how sender knows that receiver got everything

        Receiver also has some helper functions to decode and digest data, and check if packet is not corrupt

    Sender packet format: { 
                            "sequence_number": <sequence_number>, 
                            "ack": <ack>,
                            "eof": <eof>,
                            "checksum": <data_check>,
                            "data": <body>
                            }

    Receiver ack format: { 
                            "sequence_number": <sequence_number>, 
                            "next_byte_expected": <next_byte_expected>, 
                            "ack": <ack>
                        }

Challenges 

    We had challenges when figuring out what are the important things that sender and receiver need to know about their and each others current states. We ended up redoing fields that each of them need to keep track of several times. 

    It was also a little bit confusing on how to let sender know that receiver got everything, so sender can exit and don't retransmit packets.

    In addition, when trying to make protocol the most efficient we had challenges coming up with different ideas on how to do it. We ended up using dictionaries, and trying to have smart ways on checking different things

Testing
    We tested out protocol by setting different unreliable networks and with different sizes of data. We also made it appear corrupted to see if receiver catches it. We made sure our protocol is reliable when packets were getting dropped, reordered, duplicated or corrupted.


