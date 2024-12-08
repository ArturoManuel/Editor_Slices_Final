from bson import ObjectId
from pydantic import BaseModel ,  validator, Field
from typing import List , Any

class Interface(BaseModel):
    tap_name: str
    vlan: str



class UserSlice(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")  # Mapear _id a id
    id_user: str
    id_plantillas: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}  # Convierte ObjectId a string al serializar

    # Validador para manejar _id
    @classmethod
    def from_mongo(cls, document):
        document["_id"] = str(document["_id"])  # Convertir ObjectId a string
        return cls(**document)







# Definición del modelo VM
class VM(BaseModel):
    name: str
    cpu: int
    ram: str
    imagen: str
    interfaces: List[Interface]

# Definición del modelo Topología
class Topology(BaseModel):
    topologia: str
    nodos: int
    file_name: str  # Incluido en el cuerpo de la solicitud

class FileNameRequest(BaseModel):
    file_name: str

class UnionRequest(BaseModel):
    user_id: int
    topo1_name: str
    topo2_name: str
    vm1_name: str
    vm2_name: str
    vlan_union: str
    output_file_name: str  # Nuevo parámetro para el nombre del archivo de salida
    
class User(BaseModel):
    user_id: int

class CleanRequest(BaseModel):
    type: str  # 'vm', 'vlan', o 'all'

    @validator('type')
    def validate_type(cls, v):
        if v not in ['vm', 'vlan', 'all']:
            raise ValueError("type must be 'vm', 'vlan', or 'all'")
        return v