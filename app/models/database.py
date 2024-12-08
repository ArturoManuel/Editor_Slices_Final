from motor.motor_asyncio import AsyncIOMotorClient

# URL de conexión a MongoDB
MONGO_URL = "mongodb://localhost:27017"  # Cambia esto si tu base de datos está en otro servidor

# Cliente de MongoDB
client = AsyncIOMotorClient(MONGO_URL)

# Seleccionar la base de datos
db = client.Cloud
