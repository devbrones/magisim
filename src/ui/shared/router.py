import json
import redis

class Router:
    redis_client = None

    @staticmethod
    def establish_tunnel(extension_id_1, extension_id_2):
        if not Router.redis_client:
            Router.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

        Router.redis_client.set(f'connection:{extension_id_1}:{extension_id_2}', 'connected')
        Router.redis_client.set(f'connection:{extension_id_2}:{extension_id_1}', 'connected')

    @staticmethod
    def send_data(extension_id, data):
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
        if not Router.redis_client:
            raise Exception("Tunnel not established.")

        message = Router.redis_client.brpop(f'queue:{extension_id}', timeout=1)
        if message:
            _, received_message = message
            print(f"Received message by extension {extension_id}: {received_message}")
            return callback(json.loads(received_message))