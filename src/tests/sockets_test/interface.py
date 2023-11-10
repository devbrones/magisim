import os
import json
import subprocess
import yaml
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 0))
sock.listen(1)
subprocess.Popen(["python", "server.py", str(sock.getsockname()[1])])
print("Test1")
server, trash = sock.accept()
print("Test2")

with open('for_tibi/json.yml', 'r') as file:
	yml = yaml.load(file, Loader=yaml.Loader)
	with open('for_tibi/json.json', 'w') as file2:
		file2.write(json.dumps(yml, indent=4))

while True:
	inpt = input("\nAction: ")
	if (inpt == "help"):
		print("new | send | list | bind | reset")

	elif (inpt == "test"):
		server.send(bytes("interface", "utf-8"))
		msg = server.recv(1024).decode()
		print(msg)

	elif (inpt == "new"):
		inpt = input("New client name: ")
		if (inpt == "self"):
			print ("Error: Forbidden name")
			pass
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

	elif (inpt == "bind"):
		keys = sock.children.keys()

		child1 = input("Child: ")
		child2 = sock.children[keys[int(input("Bind to: "))]]
		send = {}


		if (inpt2 != "" and inpt2 != "self"):
			sock.children[inpt].send(bytes("cmd:bind", "utf-8"))
			sock.children[inpt].send(bytes("INSERT HERE: parent port", "utf-8"))
		else:
			pass

	elif (inpt == "reset"):
		keys = sock.children.keys()
		for key in keys:
			sock.children[key].send(bytes("cmd:reset", "utf-8"))