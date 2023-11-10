import os
import socket
from socketClass import socketC

os.chdir(os.path.dirname(__file__))

sock = socketC(0, False)

while True:
	inpt = input("\nAction: ")
	if (inpt == "help"):
		print("new | send | list | listen")

	elif (inpt == "new"):
		inpt = input("New client name: ")
		sock.bind(inpt)

	elif (inpt == "send"):
		inpt = input("Child: ")
		inpt2 = input("Message: ")
		if (inpt2 == ""):
			sock.children[inpt].send(bytes("Testmessage 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20", "utf-8"))
		else:
			sock.children[inpt].send(bytes(inpt, "utf-8"))

	elif (inpt == "list"):
		keys = sock.children.keys()
		for key in keys:
			print(key)