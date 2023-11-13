# imports
from shared.builtin import Extension
from shared.config import Config
from shared.settings.runtime import RuntimeSettings
from shared.item import Item
import pika

# takes an input from an extension and another extension and transports that data,
class Queue:
    pass

class RouteMap:
    nodes:[] = []
    links:[] = []



class Router:
    def map_routes(data: Item, routemap: RouteMap = RouteMap()):
        
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
                output_link_id = output_link["link"]
                outputs.append({output_name: output_link_id})
            
            routemap.nodes.append({node_id: {"inputs": inputs, "outputs": outputs}})

        return routemap


    def create_route(queue: Queue):
        
    def remove_route(queue: Queue): pass
    def get_mapped_route(me: Extension): pass
    def send(me: Extension) -> Queue: pass
    def get(me: Extension) -> Queue: pass
