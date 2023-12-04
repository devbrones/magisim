import json
import redis
from shared.item import Item

class Router:
    redis_client = None

    @staticmethod
    def establish_tunnel(extension_id_1, extension_id_2):
        """
        The function `establish_tunnel` sets up a connection between two extension IDs using Redis.
        
        :param extension_id_1: The extension ID of the first extension
        :param extension_id_2: The `extension_id_2` parameter is the ID of the second extension that you
        want to establish a tunnel with. It is used to create a unique key in Redis to represent the
        connection between the two extensions
        """
        if not Router.redis_client:
            Router.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

        Router.redis_client.set(f'connection:{extension_id_1}:{extension_id_2}', 'connected')

    @staticmethod
    def send_data(extension_id, data):
        """
        The function `send_data` sends data to connected extensions using Redis.
        
        :param extension_id: The `extension_id` parameter is a unique identifier for the extension that
        wants to send data. It is used to find the connected extensions in the Redis database
        :param data: The `data` parameter is the message or data that you want to send to the connected
        extensions. It can be of any data type, such as a string, integer, list, dictionary, etc
        """
        if not Router.redis_client:
            raise Exception("Tunnel not established.")

        connected_extensions = Router.redis_client.keys(f'connection:{extension_id}:*')
        if not connected_extensions:
            raise ValueError(f"No connected extensions found for {extension_id}")

        for connected_ext in connected_extensions:
            ext_id = connected_ext.split(b':')[-1]
            Router.redis_client.rpush(f'queue:{ext_id.decode()}', json.dumps(data))
            print(f"Sent message to extension {ext_id.decode()}: {data}")

    @staticmethod
    def receive_data(extension_id, callback):
        """
        The function `receive_data` receives messages from a Redis queue associated with a specific
        extension ID and calls a callback function with the received message as an argument.
        
        :param extension_id: The extension_id parameter is a unique identifier for the extension that is
        receiving the data. It is used to specify the Redis queue from which the data will be received
        :param callback: The `callback` parameter is a function that will be called with the received
        message as an argument. It is expected to process the received message in some way
        :return: the result of the callback function that is passed as an argument.
        """
        if not Router.redis_client:
            raise Exception("Tunnel not established.")

        message = Router.redis_client.brpop(f'queue:{extension_id}', timeout=1)
        if message:
            _, received_message = message
            print(f"Received message by extension {extension_id}: {received_message}")
            return callback(json.loads(received_message))
        
    @staticmethod
    def update_nodes(data: Item) -> tuple:
        status = ((523, "Error Processing Request")) # set default status
        routemap = []
        if data.nodes == None:
            return status
        for node in data.nodes:
            inputs: list = []
            outputs: list = []
            node_id = node["type"][-12:]
            for input_link in node["inputs"]:
                input_name = input_link["name"]
                input_link_id = input_link["link"]
                inputs.append({input_name: input_link_id})
            for output_link in node["outputs"]:
                output_name = output_link["name"]
                output_link_id = output_link["links"]
                outputs.append({output_name: output_link_id})
            routemap.append({node_id: {"inputs": inputs, "outputs": outputs}})

        print(f"DEV_DEBUGS: ROUTEMAP: {routemap}")

        


        return ((202, "Data Accepted"), routemap)

