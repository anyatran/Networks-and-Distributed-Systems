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

 	onExpiredRTOtimer() 
		// Reduce the slow start threshold using
		int flightSize = lastByteSent - lastByteAcked;
		SSThresh = flightSize / 2;
		SSThresh = Math.max(SSThresh, 2*MSS); 			

		// Perform the exponential backoff for the RTO timeout interval 
		timerBackoff();
		// and re-start the timer, for the outstanding segments.
		startRTOtimer();

		// Reset the congestion parameters
		resetParametersToSlowStart();

	timerBackoff() 
		if (timeoutInterval < maxTimeoutInterval) {
			backoff <<= 1;	// double the backoff


	resetParametersToSlowStart() 
		congWindow = MSS;
	    dupACKcount = 0;
		lastByteSentBefore3xDupAcksRecvd = -1;


	onThreeDuplicateACKs() 
		// Mark the sequence number of the last currently
		// unacknowledged byte, so that we know when all
		// currently outstanding data will be acknowledged.
		// This ACK is known as a "recovery ACK".
		// This field is used to decide when Fast Recovery should end.
		//@See TCPSenderStateFastRecovery#handleNewACK()
		if (lastByteSentBefore3xDupAcksRecvd < 0)	// if not already set:
			lastByteSentBefore3xDupAcksRecvd = lastByteSent;

		// reduce the slow start threshold
		int flightSize = lastByteSent - lastByteAcked;
		SSThresh = flightSize_ / 2;
		// Set to an integer multiple of MSS
		SSThresh -= (SSThresh % MSS);
		SSThresh = Math.max(SSThresh, 2*MSS);

		// congestion window = 1/2 FlightSize + 3xMSS:
		congWindow = Math.max(flightSize/2, 2*MSS) + 3*MSS;
		
		// Retransmit the oldest unacknowledged (presumably lost) segment.
		// Fast Retransmit
		// The timestamp of retransmitted segments should be set to "-1"
	    // to avoid performing RTT estimation based on retransmitted segments:
		oldestSegment.timestamp = -1;
	    send(oldestSegment);
	
	
