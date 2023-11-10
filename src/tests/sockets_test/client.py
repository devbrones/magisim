import sys
import json
import socket
from socketClass import socketNode

sock = socketNode(int(sys.argv[1]))

while True:
	sock.sockListen()
	#print("test")