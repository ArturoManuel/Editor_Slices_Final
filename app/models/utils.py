from bson import ObjectId

def serialize_document(document):
    """
    Serializa un documento MongoDB.
    Convierte `_id` a string y devuelve el documento modificado.
    """
    if "_id" in document:
        document["_id"] = str(document["_id"])  # Convertir ObjectId a string
    
    # Puedes agregar más lógica para estructuras específicas si es necesario
    return document

