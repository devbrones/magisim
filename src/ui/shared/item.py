from pydantic import BaseModel

class Item(BaseModel):
    last_node_id: str
    last_link_id: str
    nodes: list
    links: list
    groups: list
    config: dict
    extra: dict
    version: str
