# imports
from shared.builtin import Extension
from shared.config import Config
from shared.settings.runtime import RuntimeSettings


# takes an input from an extension and another extension and transports that data,
class Queue:
    pass

class RouteMap:
    pass


class Router:
    def map_routes(data: Item, routemap: RouteMap): pass
    def create_route(queue: Queue): pass
    def remove_route(queue: Queue): pass
    def get_mapped_route(me: Extension): pass
    def send(me: Extension) -> Queue: pass
    def get(me: Extension) -> Queue: pass
