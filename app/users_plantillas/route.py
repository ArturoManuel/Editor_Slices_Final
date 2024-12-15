from fastapi import APIRouter,  HTTPException
from app.models.models_mongodb import UsersCollection , UserSlice ,Topology , TopologyType2

from bson.objectid import ObjectId , InvalidId

from app.models.utils import serialize_document
from app.models.schema import serialize_users
#from app.models.models import UserSlice 
from fastapi.responses import JSONResponse

from app.models.database import db
from typing import List

users = APIRouter()

@users.post("/user", response_model=UserSlice)
async def create_user_slice(user_slice: UserSlice):
    # Insertar un documento en la colección
    result = await db.user_slices.insert_one(user_slice.dict())
    if result.inserted_id:
        return user_slice
    raise HTTPException(status_code=500, detail="Error al insertar el documento")



@users.delete("/user_plantillas/{id}", response_model=dict)
async def delete_plantilla(id: str):
    # Validar que el ID sea válido
    try:
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"'{id}' no es un ObjectId válido")
    
    # Intentar eliminar el documento
    result = await db.users.delete_one({"_id": object_id})

    # Verificar si se encontró y eliminó el documento
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada")
    
    # Respuesta exitosa
    return {"message": "Plantilla eliminada correctamente", "id": id}



@users.post("/user_plantillas", response_model=dict)
async def add_plantilla(data: dict):
    # Validar que el cuerpo del documento no esté vacío
    if not data:
        raise HTTPException(status_code=400, detail="Request body cannot be empty")
    
    # Validar que contenga los campos necesarios
    required_fields = ["id_user", "id_plantillas"]
    for field in required_fields:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"'{field}' is a required field")
    
    # Insertar el documento en MongoDB
    result = await db.users.insert_one(data)
    
    # Devolver el ID del documento creado
    return {"message": "Plantilla añadida", "id": str(result.inserted_id)}


@users.get("/user_plantillas/{id_user}", response_model=dict)
async def list_plantillas_by_user(id_user: str):
    # Buscar documentos en la colección 'users' con el 'id_user' proporcionado
    documents = await db.users.find({"id_user": id_user}, {"id_plantillas": 1}).to_list(1000)  # Obtener solo 'id_plantillas'
    
    # Extraer los valores de 'id_plantillas'
    plantillas = [doc["id_plantillas"] for doc in documents if "id_plantillas" in doc]
    
    # Validar si no hay resultados
    if not plantillas:
        raise HTTPException(status_code=404, detail=f"No plantillas found for user {id_user}")    
    return {"plantillas": plantillas}


@users.get("/user")
async def list_users():
    user_slices = await db.users.find().to_list(100)
    todos = serialize_users(user_slices)
    return  todos



@users.get("/plantilla/{id}")
async def get_plantilla(id: str):
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail=f"'{id}' is not a valid ObjectId")

    document = await db.plantillas.find_one({"_id": object_id})
    if not document:
        raise HTTPException(status_code=404, detail="Topology not found")

    serialized_doc = serialize_document(document)
    if "vms" in serialized_doc:
        return Topology(**serialized_doc)
    elif "topology" in serialized_doc:
        return TopologyType2(**serialized_doc)
    else:
        raise HTTPException(status_code=422, detail="Unknown document structure")  



@users.post("/plantilla", response_model=dict)
async def create_topology(data: dict):
    # Validar que el cuerpo del documento no esté vacío
    if not data:
        raise HTTPException(status_code=400, detail="Body cannot be empty")
    
    # Insertar el documento en MongoDB
    result = await db.plantillas.insert_one(data)

    # Devolver solo el ID del documento creado
    return {"message": "plantilla creada", "id": str(result.inserted_id)}


@users.put("/plantilla/{id}", response_model=dict)
async def update_topology(id: str, data: dict):
    # Validar el ID
    try:
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"'{id}' is not a valid ObjectId")
    
    # Verificar que haya datos para actualizar
    if not data:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    # Realizar la actualización
    result = await db.plantillas.update_one({"_id": object_id}, {"$set": data})

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Retornar un mensaje de éxito
    return {"message": "plantilla actualizada", "id": id}

@users.delete("/plantilla/{id}", response_model=dict)
async def delete_plantilla(id: str):
    # Validar que el ID sea válido
    try:
        object_id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"'{id}' is not a valid ObjectId")
    
    # Intentar eliminar el documento
    result = await db.plantillas.delete_one({"_id": object_id})

    # Verificar si se encontró y eliminó el documento
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Respuesta exitosa
    return {"message": "plantilla eliminida", "id": id}


@users.get("/export-plantilla/{id}", response_class=JSONResponse)
async def export_plantilla(id: str):
    try:
        # Validar el ObjectId
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")
        
        # Buscar el documento por ID
        document = await db.plantillas.find_one({"_id": ObjectId(id)})
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Convertir el ObjectId a string
        document["_id"] = str(document["_id"])
        
        # Retornar el documento como archivo JSON descargable
        return JSONResponse(
            content=document,
            headers={
                "Content-Disposition": f"attachment; filename=plantilla_{id}.json"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))