

def individual_user(user)-> dict:
    return {"id":str(user["_id"]), "id_user":str(user["id_user"]),"id_plantilla":str(user["id_plantillas"])}

def serialize_users(users)-> list:
    return [individual_user(user) for user in users]



