from pydantic import BaseModel

class Item(BaseModel):
    last_node_id: int
    last_link_id: int
    nodes: list
    links: list
    groups: list
    config: dict
    extra: dict
    version: float
