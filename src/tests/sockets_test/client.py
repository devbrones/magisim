import sys
import socket
from socketClass import socketC

sock = socketC(int(sys.argv[1]), True)

while True:
	try:
		msg = sock.main.recv(1024)
	except BlockingIOError:
		pass # No new data. Reuse old data
	else:
		if (msg == "3")
	#print("test")