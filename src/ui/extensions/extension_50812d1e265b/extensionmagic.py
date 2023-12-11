#from shared.router import Router
#
#class ExtensionMagic:
#    def __init__(self, extension_id):
#        self.extension_id = extension_id
#
#    def send_data(self, data):
#        Router.send_data(self.extension_id, data)
#
#    def receive_data(self):
#        print("got to recieve_data")
#        return Router.receive_data(self.extension_id, callback=self.callback_func)
#
#    def callback_func(self, received_data):
#        print(f"got to callback with data {received_data}")
#        return received_data
#
#    def load_data(self):
#        data = {
#            "id": self.extension_id,
#            "type": "ExtensionType",
#            "other_data": "Other relevant information"
#        }
#        self.send_data(data)
#
## Instantiate your extension with the given UUID
#exmag = ExtensionMagic("50812d1e265b") ## uuids are stripped to last 12 anums for compability and readability
#
#
#def run_extension():
#    return exmag.receive_data()

def run_extension():
    return "Hello from ExtensionMagic!"