from shared.router import Router

class OpenMSEMS:
    def __init__(self, extension_id):
        self.extension_id = extension_id

    def send_data(self, data):
        Router.send_data(self.extension_id, data)

    def receive_data(self):
        return Router.receive_data(self.extension_id, callback=self.callback_func)

    def callback_func(self, received_data):
        return received_data

    def load_data(self):
        data = {
            "id": self.extension_id,
            "type": "ExtensionType",
            "other_data": "Other relevant information"
        }
        self.send_data(data)

# Instantiate your extension with the given UUID
openmsems_ext = OpenMSEMS("caed19de0a8b") ## uuids are stripped to last 12 anums for compability and readability

# Call the load_data function to send data
def sendtest():
    openmsems_ext.load_data()

