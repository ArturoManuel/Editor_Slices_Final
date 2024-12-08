from fastapi import APIRouter, Path ,status , HTTPException ,Body
from app.models.models import VM, Topology , FileNameRequest ,UnionRequest ,User ,CleanRequest
from app.gestionar_vm.gestion import (add_vm, create_topology,get_vm_count, 
                                        clear_vms ,list_files_by_user,
                                        get_topology_from_file, delete_topology_file,
                                        unir_topologias , delete_topologies_by_user ,clear_topology_data)


vm_router = APIRouter()

# Endpoint para agregar una VM para un usuario específico
@vm_router.post("/add_vm/{user_id}")
async def add_vm_endpoint(vm: VM, user_id: int = Path(..., description="ID del usuario")):
    added_vm = add_vm(user_id, vm)
    if "error" in added_vm:
        raise HTTPException(status_code=400, detail=added_vm["error"])
    return {"message": f"VM agregada exitosamente para el usuario {user_id}", "vm": added_vm}

@vm_router.get("/vm_count/{user_id}")
async def vm_count_endpoint(user_id: int = Path(..., description="ID del usuario")):
    count, vms = get_vm_count(user_id)
    if count > 0:
        return {"message": f"Hay {count} VM(s) para el usuario {user_id}", "vms": vms}
    else:
        return {"message": f"No hay VMs para el usuario {user_id}"}


@vm_router.post("/clear_vms")
async def clear_vms_endpoint(request: User):
    clear_vms(request.user_id)
    return {"message": f"Todas las VMs han sido eliminadas para el usuario {request.user_id}"}

# Endpoint para crear la topología con las VMs del usuario
@vm_router.post("/create_topology/{user_id}", status_code=status.HTTP_201_CREATED)
async def create_topology_endpoint(user_id: int, topology: Topology):
    # Aquí podrías incluir una verificación si user_id es válido o no
    # Si user_id no es válido, puedes levantar una excepción HTTP
    print(topology)
    topology_json = create_topology(user_id, topology)
    if 'error' in topology_json:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=topology_json['error'])

    return {"message": f"Topología '{topology.file_name}' creada exitosamente para el usuario {user_id}"}

# Endpoint para verificar la cantidad de VMs en el diccionario para un usuario específico


# Endpoint para limpiar las VMs del diccionario para un usuario específico



@vm_router.get("/list_slices/{user_id}")
async def list_slices(user_id: int = Path(..., description="ID del usuario")):
    # Listar archivos JSON para el usuario
    files = list_files_by_user(user_id)
    
    if files:
        return {"message": f"Archivos de slices para el usuario {user_id}", "files": files}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron slices para el usuario.")

@vm_router.post("/get_slice/")
async def get_slice(file_request: FileNameRequest):
    # Usar directamente el nombre del archivo proporcionado
    file_name = file_request.file_name
    topology_data = get_topology_from_file(file_name)
    
    if 'error' in topology_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=topology_data['error'])

    return {"message": f"Contenido del archivo '{file_name}'", "topology_data": topology_data}

@vm_router.post("/delete_slice/")
async def delete_slice(file_request: FileNameRequest):
    # Usar directamente el nombre del archivo proporcionado
    file_name = file_request.file_name
    delete_response = delete_topology_file(file_name)  # Llamar a la función para eliminar el archivo
    
    if 'error' in delete_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=delete_response['error'])

    return {"message": delete_response['message']}


@vm_router.post("/delete_user_slices/")
async def delete_user_slices(request: User):
    delete_response = delete_topologies_by_user(request.user_id)
    
    if 'error' in delete_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=delete_response['error'])

    return {"message": delete_response['message']}

@vm_router.post("/clear_topology_data/")
async def clear_topology_endpoint(request: CleanRequest):
    clear_results = clear_topology_data(request.type)
    if all(res.endswith("successfully") for res in clear_results.values()):
        return {"message": "Requested data cleared successfully", "details": clear_results}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=clear_results)
    

@vm_router.post("/unir_topologias/", status_code=status.HTTP_201_CREATED)
async def unir_topologias_endpoint(union_request: UnionRequest):
    """
    POST para unir dos topologías.
    """
    user_id = union_request.user_id
    topo1_name = union_request.topo1_name
    topo2_name = union_request.topo2_name
    vm1_name = union_request.vm1_name
    vm2_name = union_request.vm2_name
    vlan_union = union_request.vlan_union
    output_file_name = union_request.output_file_name  # Recibir el nombre del archivo de salida

    # Llamar a la función para unir las topologías
    response = unir_topologias(user_id, topo1_name, topo2_name, vm1_name, vm2_name, vlan_union, output_file_name)
    
    if "error" in response:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=response["error"])
    
    return {"message": response["message"], "file": response["file"]}
