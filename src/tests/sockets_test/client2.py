import sys
import socket
from socketClass import socketNode

sock = socketNode(int(sys.argv[1]), True)

while True:
	try:
		msg = sock.main.recv(1024)
	except BlockingIOError:
		pass # No new data. Reuse old data
	else:
		print(msg.decode("utf-8"))
	#print("test")