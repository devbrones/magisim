import os
import sys
import json
import socket
from socketClass import socketNode

os.chdir(os.path.dirname(__file__))

sock = socketNode(int(sys.argv[1]), blocking=True)

def printc(out: str) -> None:
	sock.main.send(bytes(out, "utf-8"))

while True:
	sock.sockListen()

	# Temp code below

	try:
		inpt = json.loads(sock.main.recv(1024).decode())
	except BlockingIOError:
		pass # No new data. Reuse old data
	else:
		if (inpt["mode"] == "help"):
			printc("new | send | list | bind | reset")

		elif (inpt["mode"] == "new"):
			if (inpt["name"] == "self"):
				printc ("Error: Forbidden name")
				pass
			sock.bind(inpt["name"])

		elif (inpt["mode"] == "send"):
			if (inpt["message"] == ""):
				sock.children[inpt["child"]].send(bytes("Testmessage 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20", "utf-8"))
			else:
				sock.children[inpt["child"]].send(bytes(inpt["name"], "utf-8"))

		elif (inpt["mode"] == "list"):
			keys = sock.children.keys()
			for key in keys:
				printc(key)

		elif (inpt["mode"] == "bind"):
			keys = sock.children.keys()

			if (inpt["node1"] == "" or inpt["node1"] == "manager"):
				pass
			else:
				sendInfo = { "mode": "bind" }
				#sendInfo["node1"] = inpt["node1"]
				sock.children[inpt["node1"]].send(bytes(json.dumps(sendInfo), "utf-8"))


			if (inpt["node2"] == "" or inpt["node2"] == "manager"):
				pass
			else:
				sendInfo = { "mode": "connect" }
				sendInfo["node1"] = inpt["node1"]
				sock.children[inpt["node2"]].send(bytes(json.dumps(sendInfo), "utf-8"))
				pass
				sendInfo["node1"] = inpt["node1"]
				sendInfo["node2"] = inpt["node2"]
				sock.children[inpt["node1"]].send(bytes(json.dumps(sendInfo), "utf-8"))
				sock.children[inpt["node2"]].send(bytes(json.dumps(sendInfo), "utf-8"))

		elif (inpt == "reset"):
			keys = sock.children.keys()
			for key in keys:
				sock.children[key].send(bytes("cmd:reset", "utf-8"))