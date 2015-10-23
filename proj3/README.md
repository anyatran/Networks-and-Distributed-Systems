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
	}

