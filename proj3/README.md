<b> REQUIREMENTS\: </b><br/>
    - command syntax\: ./3700send \<recv_host\>\:\<recv_port\> <br/>
    - The sender must accept data from STDIN, sending data until EOF is reached<br/>
    - The sender and receiver must work together to transmit the data reliably<br/>
    - The receiver must print out the received data to STDOUT in order and without errors<br/>
    - The sender and receiver must print out specified debugging messages to STDERR<br/>
    - Your sender and receiver must gracefully exit<br/>
    - Your code must be able to transfer a file with any number of packets dropped, damaged, duplicated, and delayed, and under a variety of different available bandwidths and link latencies<br/>
    - Your sending program must be named 3700send and your receiving program must be named 3700recv<br/>



 questions:

 SENDER
 constantly listen for RTO time expiration and retransmit?? or what is the case with selective ack
 constantly listen for three duplicates acks?
 how to know when sending a packet if it's initial send or retransmit
 main functions:
 send_data
 process_ack
 calculate_timeout


 RECEIVER
 receiver must print out data in order - how to keep track of ordered packets?
 selective ACK -? 
 what do we need to keep track of in receiver?
 main functions:
 send_ack
 receive

	resetParametersToSlowStart() 
		congWindow = MSS;
	    dupACKcount = 0;
		lastByteSentBefore3xDupAcksRecvd = -1;


receiver:
	buffer = []						for out of order packets, should be in ascending order by sequence number to fill in gaps later
	last_byte_recv = -1  			last byte received in sequence
	next_byte_expected = 0
	rcv_window

	process_data_segment(segment)
		if (check_data(segment)):
			return

		# if segment arrived in order
		if (segment["sequence_number"] == next_byte_expected):
			next_byte_expected = segment["sequence_number"] + len(segment) # or MSS or 1500?

			if (len(buffer) < 0):
				# No previously buffered segments.
				last_byte_recvd = segment["sequence_number"] + len(segment) - 1;

			else:
				# Some segments were previously buffered.
				# Checked whether this segment filled any gaps for
				# the possible buffered segments.  If yes,
				# this will update "last_byte_recv"
				check_buffered();


			ack = {adv_w: current_rcv_w, sequence_number: next_byte_expected, timestamp: segment["timestamp"]}


		else:
			# should we buffer them?? 
			process_out_of_order_data_segment(segment)


	process_out_of_order_data_segment(segment):

		buffer.add(segment)

		# Also, we CANNOT assume that all currently buffered segments
		# have sequence number lower than the one that just arrived.
		last_byte_recv = max(last_byte_recv, segment["sequence_number"] + len(segment) - 1)

		# should we reduce our window?? even though we are not using it yet.. 
		rcv_window = max_rcv_window - (last_byte_recv - next_byte_expected)

		ack = {adv_w: rcv_window, sequence_number: next_byte_expected, timestamp: -1} # -1 or what?



        


#calculates estimated timeout time based on RTTs
#Inputs: SampleRTT, old estimatedRTT, alpha
# def estimate_timeout(timestamp, old_rtt):
#     sample_rtt = time.time() - timestamp #current_time - timestamp
#     estimated_rtt = (1 - ALPHA) * old_rtt * (0.875 * ALPHA)
#     return estimated_rtt

## calculates congestion window
## call it when NEW ack was received
# def calc_congestion_window_after_new_ack():
    # global CONGESTION_WIN

    # if (CONGESTION_WIN < SSTHRESH):
    #     #slow start
    #     CONGESTION_WIN = CONGESTION_WIN + 1 ##?????????? or cwnd = cwnd + MSS
    # ## congestion avoidance
    # else:
    #     CONGESTION_WIN = CONGESTION_WIN + (1/CONGESTION_WIN) ##?????????? or cwnd = cwnd+ mss*(mss/cwnd)

## if duplicate or old ack:
# if tcp.ack==snd.una:    # duplicate acknowledgement
#     dupacks++
#     if dupacks==3:
#       retransmitsegment(snd.una)
#       ssthresh=max(cwnd/2,2*MSS)
#       cwnd=ssthresh
#   else:    # ack for old segment, ignored
#     dupacks=0

# def send_next_packet(data):
#     global SEQUENCE
#     global lastByteSent

#     if (len(data) > 0):
#               ## binary encode
#           msg = json.dumps({"sequence": SEQUENCE, "data": data, "ack": False, "eof": False}) #, "digested": digest_data(data)})
#           SEQUENCE += len(data)
#           log("[sequence n] " + str(SEQUENCE))

#           if sock.sendto(msg, dest) < len(msg):
#           log("[error] unable to fully send packet")
#           else:
#               lastByteSent += len(data)
#               log("[last byte sent] " + str(lastByteSent))
#           log("[send data] " + str(SEQUENCE) + " (" + str(len(data)) + ")")
#           return True
#     else:
#           return False







    # def process_corrupted_data(self, packet):
    #     log("[CORRUPTED] " + str(packet["sequence_number"]))
    #     self.send_dack(self.next_byte_expected, packet["timestamp"])
        
    # def process_out_of_order_data_segment(packet):
    #     log("[OUT OF ORDER] " + str(packet["sequence_number"]))
    #     self.send_dack(packet["timestamp"])
        #self.buffered_segments.add(packet)

        # Also, we CANNOT assume that all currently buffered segments
        # have sequence number lower than the one that just arrived.
        #self.last_byte_rcv = max(self.last_byte_rcv, packet["sequence_number"] + len(packet["data"]) - 1)

        # should we reduce our window?? even though we are not using it yet.. 
        # self.rcv_window = self.max_rcv_window - (self.last_byte_rcv - self.next_byte_expected)
        #ack = {"adv_w": self.rcv_window, "sequence_number": self.next_byte_expected, timestamp: -1} # -1 or what?







     def send(self):
        if (len(s.data) > 0):
            ## 1. How many segments are currently unacknowledged
            flight_size = self.last_byte_sent - self.last_byte_acked
            ## 2. How many segments can still be sent - usable window
            effective_window = self.cong_window - flight_size ### or min(self.cong_window, self.recv_window)
            if (effective_window < 0):
                effective_window = 0
            log("[congestion window]=" + str(self.cong_window) + " [recv_window]=" + str(self.recv_window) + "[effective window]=" + str(effective_window) + "[flight size]=" + str(flight_size))
            burst_size = effective_window / MSS ##, ##remaining data - len(data[lastByteSent:])? / MSS);
            log("[burst size]=" + str(burst_size))
            if (burst_size > 0): 
                ## Send the "burstSize" worth of segments:
                i = 0
                while (i < burst_size) :
                    ##Extract one segment of data
                    packet = self.create_packet() 
                    #log("[created this packet]=" + str(packet))

                    if sock.sendto(packet, dest) < len(packet):
                        log("[error] unable to fully send packet")
                    else:
                        log("[send data] " + str(self.last_byte_sent) + " (" + str(len(packet)) + ")")
                        timeout = self.calc_timeout()
                        self.sent_data[self.last_byte_sent] = {"sent": True, "timeout": timeout, "sent_time": time.time()}
                        self.acked_data[self.last_byte_sent] = False
                        #Timer(timeout, self.fast_retransmit, [self.last_byte_sent]).start()
                        #self.last_byte_sent += MSS
                        #log("[last byte sent after sending packet]=" + str(self.last_byte_sent))
                    i = i + 1



        def create_packet(self):
        segment = s.data[self.last_byte_sent: self.last_byte_sent + MSS]
        if (((self.last_byte_sent + MSS) / MSS) >= ((len(s.data)) / MSS)):
            log("[SENDING LAST PIECE]")
            eof = True
        else:
            eof = False
        ack = False
        flags = (eof << 1) + ack
        digested = self.digest_data([self.last_byte_sent, flags, segment])
        tcp_header = struct.pack("!LH16s", self.last_byte_sent, flags, digested)
        #log("[last byte sent]=" + str(self.last_byte_sent) + " ack=" + str(ack) + " eof=" + str(eof) + " segment check=" + str(digested) + " header_size=" + str(struct.calcsize("!LH16s")))
        #log("[tcp header]=" + tcp_header)
        data_packet = tcp_header + segment
        return data_packet






            # def process_dup_ack(self, packet):
    #     self.dup_ack_count = self.dup_ack_count + 1
    #     if (self.dup_ack_count >= 3):
    #         self.fast_retransmit(packet)

    # def process_ack(self, packet):
    #     log("[recv ack] " + str(packet["sequence_number"]))
    #     self.RTT = time.time() - self.sent_data[packet["sequence_number"]]['sent_time']
    #     self.acked_data[packet["sequence_number"]] = True
    #     #self.last_byte_acked = packet["sequence_number"]
    #     log("[got ack with sequence number]=" + str(packet["sequence_number"]))
    #     log("[my last_byte_acked]=" + str(self.last_byte_acked))
    #     if (packet["sequence_number"] == self.last_byte_acked):
    #         ## figure out current state and process new ack accordingly
    #         self.process_new_ack(packet)
    #         # If all outstanding data at 3 dupACKs have been acked, reset the indicator parameter.
    #         if (self.last_byte_sent_before_3dup_acks <= self.last_byte_acked):
    #             self.last_byte_sent_before_3dup_acks = -1          
    #     ## If duplicate ack
    #     else:
    #         ## figure out current state and process dup ack accordingly
    #         self.process_dup_ack(packet)
