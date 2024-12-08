from fastapi import FastAPI
from app.gestionar_vm.route import vm_router
from app.users.route import users

app = FastAPI()

app.include_router(vm_router)
app.include_router (users)



