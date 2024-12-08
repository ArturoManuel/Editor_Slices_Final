import json
from app.models.models import VM, Topology
import os

# Diccionario para almacenar las VMs por usuario
# Las claves serán los IDs de usuario, y los valores serán listas de VMs
user_vms = {}

# Agregar VM para un usuario específico
def add_vm(user_id: int, vm: VM):
    if user_id not in user_vms:
        user_vms[user_id] = []
    user_vms[user_id].append(vm.dict())
    return vm.dict()
# Obtener la cantidad de VMs para un usuario específico
def get_vm_count(user_id: int):
    if user_id in user_vms:
        return len(user_vms[user_id]), user_vms[user_id]
    return 0, []

# Limpiar las VMs para un usuario específico
def clear_vms(user_id: int):
    if user_id in user_vms:
        user_vms[user_id].clear()




# Crear la topología para un usuario específico
def create_topology(user_id: int, topology: Topology):
    if user_id not in user_vms or not user_vms[user_id]:
        return {"error": "No hay VMs para este usuario"}
    topology_data = {
        "topologia": topology.topologia,
        "nodos": topology.nodos,
        "vms": user_vms[user_id]
    }
    
    # Asegurarse de que exista el directorio de datos
    if not os.path.exists('data'):
        os.makedirs('data')

    file_name = f"data/{user_id}_{topology.file_name}.json"

    try:
        with open(file_name, "w") as f:
            json.dump(topology_data, f, indent=4)
        # Actualizar la información de VLAN utilizando la función save_vlan_info
        save_vlan_info(user_id, user_vms[user_id])
        save_vm_info(user_id, user_vms[user_id])
    except Exception as e:
        return {"error": f"Error al guardar los archivos JSON: {e}"}

    # Limpiar las VMs del usuario después de crear la topología
    user_vms[user_id].clear()
    return {"message": f"Archivo de topología y VLAN actualizados para el usuario {user_id}"}


def save_vm_info(user_id: int, vms: list):
    vm_file_name = "data/vms.json"
    
    # Cargar los datos existentes de VMs si el archivo existe, si no, usar un diccionario vacío
    if os.path.exists(vm_file_name):
        with open(vm_file_name, "r") as file:
            vm_data = json.load(file)
    else:
        vm_data = {}
    
    # Actualizar o añadir nuevas entradas de VMs
    for vm in vms:
        vm_data[vm['name']] = {
            "user_id": user_id,
            "interfaces": vm['interfaces']
        }

    # Guardar la información actualizada de vuelta en el archivo
    with open(vm_file_name, "w") as file:
        json.dump(vm_data, file, indent=4)



def save_vlan_info(user_id: int, vms: list):
    vlan_file_name = "data/vlan.json"
    
    # Cargar los datos existentes de VLANs si el archivo existe, si no, usar un diccionario vacío
    if os.path.exists(vlan_file_name):
        with open(vlan_file_name, "r") as file:
            vlan_data = json.load(file)
    else:
        vlan_data = {}
    
    # Actualizar o añadir nuevas entradas de VLANs
    for vm in vms:
        for interface in vm['interfaces']:
            vlan_id = interface['vlan']
            vlan_data.setdefault(vlan_id, []).append({
                "user_id": user_id,
                "vm_name": vm['name'],
                "interface_name": interface['tap_name']
            })

    # Guardar la información actualizada de vuelta en el archivo
    with open(vlan_file_name, "w") as file:
        json.dump(vlan_data, file, indent=4)



def list_files_by_user(user_id: int):
    # Verificar si el directorio 'data' existe
    if not os.path.exists('data'):
        return []

    # Listar todos los archivos en la carpeta 'data'
    files = os.listdir('data')

    # Filtrar archivos que comiencen con el user_id seguido de un guión bajo y que terminen en .json
    user_files = [f for f in files if f.startswith(f"{user_id}_") and f.endswith(".json")]
    
    return user_files


def get_topology_from_file(filename: str):
    try:
        file_path = os.path.join('data', filename)
        if not os.path.exists(file_path):
            return {"error": "Archivo no encontrado"}
        with open(file_path, 'r') as f:
            topology_data = json.load(f)
        return topology_data
    except Exception as e:
        return {"error": f"Error al leer el archivo: {e}"}


def delete_topology_file(filename: str):
    try:
        file_path = os.path.join('data', filename)
        
        # Verificar si el archivo existe
        if os.path.exists(file_path):
            os.remove(file_path)
            return {"message": f"El archivo '{filename}' ha sido eliminado exitosamente."}
        else:
            return {"error": "Archivo no encontrado"}
    except Exception as e:
        return {"error": f"Error al eliminar el archivo: {e}"}
    



def clear_topology_data(clean_type: str):
    paths = {
        'vm': "data/vms.json",
        'vlan': "data/vlan.json"
    }
    results = {}

    if clean_type == 'all':
        files_to_clear = paths.values()
    else:
        files_to_clear = [paths[clean_type]]

    for file_name in files_to_clear:
        try:
            if os.path.exists(file_name):
                with open(file_name, 'w') as file:
                    json.dump({}, file)
                results[file_name] = "Cleared successfully"
            else:
                results[file_name] = "File not found"
        except Exception as e:
            results[file_name] = f"Error clearing the file: {e}"

    return results




def delete_topologies_by_user(user_id: int):
    directory = 'data'
    deleted_files = []
    error_messages = []

    # Listar todos los archivos en el directorio 'data'
    try:
        files = os.listdir(directory)
        # Filtrar archivos que comiencen con el user_id especificado
        user_files = [file for file in files if file.startswith(f"{user_id}_") and file.endswith(".json")]

        if not user_files:
            return {"error": "No se encontraron archivos para el usuario especificado."}

        # Eliminar archivos filtrados
        for file in user_files:
            try:
                os.remove(os.path.join(directory, file))
                deleted_files.append(file)
            except Exception as e:
                error_messages.append(f"Error al eliminar el archivo {file}: {e}")

        if error_messages:
            return {"error": "Algunos archivos no pudieron ser eliminados.", "details": error_messages}

        return {"message": f"Los archivos {', '.join(deleted_files)} han sido eliminados exitosamente."}
    except Exception as e:
        return {"error": f"Error al listar o eliminar archivos: {e}"}



def unir_topologias(user_id: int, topo1_name: str, topo2_name: str, vm1_name: str, vm2_name: str, vlan_union: str, output_file_name: str):
    """
    Función para unir dos topologías y generar un nuevo archivo JSON con la unión, con un nombre de archivo personalizado.
    """
    
    # Listar archivos del usuario para encontrar las topologías
    files = list_files_by_user(user_id)
    topo1_file = None
    topo2_file = None

    # Buscar los archivos de las topologías especificadas
    for file in files:
        if file.startswith(f"{user_id}_{topo1_name}.json"):
            topo1_file = file
        elif file.startswith(f"{user_id}_{topo2_name}.json"):
            topo2_file = file

    if not topo1_file or not topo2_file:
        return {"error": "Una o ambas topologías no fueron encontradas"}

    # Obtener las topologías desde los archivos
    topo1_data = get_topology_from_file(topo1_file)
    topo2_data = get_topology_from_file(topo2_file)

    if "error" in topo1_data or "error" in topo2_data:
        return {"error": "Error al leer una de las topologías"}

    # Buscar las VMs en las topologías
    vm1_data = next((vm for vm in topo1_data['vms'] if vm['name'] == vm1_name), None)
    vm2_data = next((vm for vm in topo2_data['vms'] if vm['name'] == vm2_name), None)

    if not vm1_data:
        return {"error": f"La VM {vm1_name} no fue encontrada en la topología {topo1_name}"}
    if not vm2_data:
        return {"error": f"La VM {vm2_name} no fue encontrada en la topología {topo2_name}"}

    # Verificar que la VLAN de unión no exista en ninguna de las interfaces de las VMs
    for interface in vm1_data['interfaces'] + vm2_data['interfaces']:
        if interface['vlan'] == vlan_union:
            return {"error": f"La VLAN {vlan_union} ya está en uso en una de las VMs"}

    # Añadir la interfaz de unión a vm1 y vm2
    vm1_data['interfaces'].append({
        "tap_name": f"tap-{vm1_name}-{vlan_union}",
        "vlan": vlan_union
    })
    vm2_data['interfaces'].append({
        "tap_name": f"tap-{vm2_name}-{vlan_union}",
        "vlan": vlan_union
    })

    # Unir las VMs de ambas topologías en un solo diccionario de VMs
    unified_vms = topo1_data['vms'] + topo2_data['vms']

    # Crear la nueva topología unificada
    new_topology = {
        "topologia": f"{topo1_data['topologia']}-{topo2_data['topologia']}",
        "nodos": len(unified_vms),
        "vms": unified_vms
    }

    # Guardar el nuevo archivo JSON con la unión de las topologías
    # Usar el nombre del archivo proporcionado (output_file_name)
    file_path = os.path.join('data', f"{user_id}_{output_file_name}.json")
    
    try:
        with open(file_path, 'w') as f:
            json.dump(new_topology, f, indent=4)
    except Exception as e:
        return {"error": f"Error al escribir el archivo unificado: {e}"}

    return {"message": f"Topologías '{topo1_name}' y '{topo2_name}' unidas exitosamente", "file": f"{user_id}_{output_file_name}.json"}

