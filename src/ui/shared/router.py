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

        # create actual nodemap, but exclude all the null connections
        # Initialize lists to store node IDs and connections
        node_ids = []
        connections = []
        print(f"DEV_DEBUGS: rmap ::::: {routemap}")
        # Iterate over the routemap
        for node_data in routemap:
            node_id = next(iter(node_data))  # Extract the 12-character node ID
            print(f"DEV_DEBUGS: working nodeid: {node_id}")
            node_ids.append(node_id)

            non_none_inputs = [
                (k, next(iter(input_dict.values()))) for input_dict in node_data[node_id]['inputs'] 
                for k, v in input_dict.items() 
                if v is not None and isinstance(next(iter(input_dict.values())), int)
            ]
            non_none_outputs = [
                (k, next(iter(output_dict.values()))) for output_dict in node_data[node_id]['outputs']
                for k, v in output_dict.items() 
                if v is not None and (isinstance(next(iter(output_dict.values())), int) or isinstance(next(iter(output_dict.values())), list))
            ]

            input_ids = [input_id for input_id, value in non_none_inputs if len(input_id) == 12]
            output_ids = [output_id for output_id, value in non_none_outputs if len(output_id) == 12]
            
            print(f"DEV_DEBUGS: ioids: {input_ids} :: {output_ids}")

            for input_id in input_ids:
                for output_id in output_ids:
                    connections.append((input_id, output_id))     

        print(f"DEV_DEBUGS: GOT PAST IT ALL FUCK YEA")
        for input_id, output_id in connections:
            print(f"DEV_DEBUGS: CONNECTION {input_id}, {output_id}")

        print(f"DEV_DEBUGS: WHAT IN GODS NAME {connections}")


        return ((202, "Data Accepted"), routemap)

