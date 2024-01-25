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

        redstring = f'connection>{extension_id_1}>{extension_id_2}' # > is used as a delimiter
        Router.redis_client.set(redstring, 'connected')

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
        status = ((523, "Error Processing Request"))  # set default status
        routemap = []
        if data.nodes is None:
            return status

        for node in data.nodes:
            node_id = node["type"][-12:]
            # Use get method with default value to handle missing 'inputs'
            inputs = [{input_link["name"]: input_link["link"]} for input_link in node.get("inputs", [])]

            # Check if the node has outputs
            if "outputs" not in node or node["outputs"] == "":
                routemap.append({node_id: {"inputs": inputs, "outputs": None}})
                continue

            outputs = [{output_link["name"]: output_link["links"]} for output_link in node["outputs"]]
            routemap.append({node_id: {"inputs": inputs, "outputs": outputs}})

        print(f"DEV_DEBUGS: ROUTEMAP: {json.dumps(routemap, indent=4, sort_keys=True)}")
        return ((202, "Data Accepted"), routemap)
    
    @staticmethod
    def route(data: Item):
        # get the current routemap
        route_map = Router.update_nodes(data)[1]
        # iterate through the routemap and establish connections between the nodes that are connected, 
        # in the order that they are connected (out->in), some nodes wont have an output attached (no "outputs" key at all), they would be the last in a chain
        # and they need to be notified that they are.
        # for now we will just print the connections in the format "(uuid_1) -> (uuid_2)"
        # Dictionary to hold the mapping of UUIDs to their inputs
        uuid_inputs = {}

        # Populate the inputs, handling missing 'inputs' key
        for item in route_map:
            for uuid, content in item.items():
                for input_item in content.get("inputs", []):
                    for input_key, input_value in input_item.items():
                        if uuid not in uuid_inputs:
                            uuid_inputs[uuid] = []
                        uuid_inputs[uuid].append((input_key, input_value))

        # Set to hold UUIDs which have outputs and a separate set for those with inputs
        uuids_with_output = set()
        uuids_with_input = set(uuid_inputs.keys())

        # Establish and print connections based on outputs, handling missing 'outputs' key
        for item in route_map:
            for uuid, content in item.items():
                if 'outputs' in content and content["outputs"] is not None:
                    uuids_with_output.add(uuid)
                    for output in content["outputs"]:
                        for output_key, output_value in output.items():
                            if isinstance(output_value, list):
                                # Find the corresponding input UUID and print the connection
                                for val in output_value:
                                    for input_uuid, input_values in uuid_inputs.items():
                                        for input_key, input_val in input_values:
                                            if val == input_val:
                                                connection1 = f"{uuid}:{output_key}:{val}"                  #
                                                connection2 = f"{input_uuid}:{input_key}:{input_val}"       # : is used as a delimiter
                                                print(f"{connection1} -> {connection2}")
                                                Router.establish_tunnel(connection1, connection2)           # establish a tunnel between the two nodes

        # Identify and print nodes that are at the end of a chain (without outputs) or start of a chain (without inputs)
        all_uuids = set(uuids_with_input.union(uuids_with_output))
        for uuid in all_uuids:
            if uuid not in uuids_with_output:
                print(f"{uuid} is the end of a chain")
            if uuid not in uuids_with_input:
                print(f"{uuid} is the start of a chain")


        



