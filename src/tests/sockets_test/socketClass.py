import socket

class socketC:
    def __init__(self, port, temp: bool) -> None:
        self.main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.parents: dict[str, socket.socket] = {} # Only used for nodes
        self.children: dict[str, socket.socket] = {}
        if (temp):
            self.s.connect((socket.gethostname(), port))
            self.s.setblocking(False)

    def connect(self, port: int) -> None:
        self.s.connect(("", port))

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