from bson.objectid import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional
# Modelo que mapea _id como string
class UserSlice(BaseModel):
    id_user: Optional[str]  
    id_plantillas: Optional[str]  


    
class UsersCollection(BaseModel):
    users: List[UserSlice]



class Interface(BaseModel):
    tap_name: str
    vlan: str

class VM(BaseModel):
    name: str
    cpu: int
    ram: str
    imagen: str
    interfaces: List[Interface]



class Topology(BaseModel):
    id: str = Field(alias="_id")  # Mapear _id a id
    topologia: str
    nodos: int
    vms: List[VM]
    servicio: str
    name: str

    class Config:
        populate_by_name = True  # Permitir usar alias





# Modelo para el segundo tipo
class Link(BaseModel):
    link_id: str
    source: str
    target: str

class Node(BaseModel):
    node_id: str
    name: str
    access_protocol: str
    cpu: int
    image: str
    memory: float
    security_rules: List[int]
    storage: int

class TopologyType2(BaseModel):
    id: str = Field(alias="_id")
    name: str
    topology: dict
    servicio: str