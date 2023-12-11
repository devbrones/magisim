#from shared.router import Router
#class Visualizer:
#    def __init__(self, extension_id):
#        self.extension_id = extension_id
#
#    def send_data(self, data):
#        Router.send_data(self.extension_id, data)
#
#    def receive_data(self):
#        return Router.receive_data(self.extension_id, callback=self.callback_func)
#
#    def callback_func(self, received_data):
#        return received_data
#
#    def load_data(self,data):
#        self.send_data(data)
#
#vis = Visualizer("61c6599e8f96")
#
#def get_visualizer(app):
#    # check for new data in the tunnel
#    data = None
#    while not data:
#        data = vis.receive_data()
#    # we recieved new data
    


