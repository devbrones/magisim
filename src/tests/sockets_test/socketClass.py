import json
import socket

class socketNode:
	def __init__(self, port, blocking=False) -> None:
		self.main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.parents: dict[str, socket.socket] = {} # Only used for nodes
		self.children: dict[str, socket.socket] = {}
		self.main.connect((socket.gethostname(), port))
		self.main.setblocking(blocking)

	def connect(self, port: int) -> None:
		self.main.connect(("", port))

	def bind(self, child:str):
		self.children[child] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.children[child].bind((socket.gethostname(), 0))
		print(self.children[child].getsockname()[1])
		self.children[child].listen(1)
		childSock, trash = self.children[child].accept()
		self.children[child] = childSock
	
	def reset(self):
		keys = self.children.keys()
		for key in keys:
			self.children[key].close()
			del self.children[key]

		keys = self.parents.keys()
		for key in keys:
			self.parents[key].close()
			del self.parents[key]

	def sockListen(self):
		try:
			msg = self.main.recv(1024).decode()
		except BlockingIOError:
			pass # No new data. Reuse old data
		else:
			if (msg == "cmd:reset"):
				print("cmd:reset")
				self.reset()
			elif (msg == "cmd:bind"):
				print("cmd:bind")
				self.main.setblocking(True)
				msg: dict[str, str] = json.loads(self.main.recv(1024).decode())

				print(msg)
				
				""" if (msg["mode"] == "parent"):
					self.parents[msg2["name"]].close()

				elif (msg1 == "mode:child"):
					self.parents[msg2["name"]] """
				self.main.setblocking(False)