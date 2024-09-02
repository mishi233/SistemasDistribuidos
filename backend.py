from fastapi import FastAPI, APIRouter, HTTPException, Body, Path
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel

# Obtener la URL de MongoDB desde las variables de entorno
mongo_url = "mongodb+srv://michaelromero:mishi233@cluster0.jwyyl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Imprimir el URI de conexión para verificación
print(f"Conectando a MongoDB en: {mongo_url}")

# Crear la aplicación FastAPI
app = FastAPI()

origins = [
    "http://localhost:4200",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a MongoDB
client = MongoClient(mongo_url)
database = client["database1"]
collection = database["collection1"]

# Modelos Pydantic
class Nombre(BaseModel):
    nombre: str

class UpdateNombre(BaseModel):
    nombreActual: str
    nuevoNombre: str


# Función para serializar los objetos de MongoDB
def serialize_nombre(item) -> dict:
    return {
        "nombre": item["nombre"]
    }

# Servicio General
class GeneralService:
    def obtener_nombres(self):
        items = collection.find()
        listaNombres = []
        for item in items:
            listaNombres.append(serialize_nombre(item)["nombre"])
        return listaNombres

    def agregar_nombre(self, nombre: str):
        result = collection.insert_one({"nombre": nombre})
        return serialize_nombre(collection.find_one({"_id": result.inserted_id}))

    def actualizar_nombre(self, nombre_actual: str, nuevo_nombre: str):
        result = collection.update_many({"nombre": nombre_actual}, {"$set": {"nombre": nuevo_nombre}})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Nombre not found")
        return {"message": f"Updated {result.modified_count} names from '{nombre_actual}' to '{nuevo_nombre}'"}

    def borrar_nombre(self, nombre: str):
        result = collection.delete_many({"nombre": nombre})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Nombre not found")
        return {"message": f"Deleted {result.deleted_count} names with the name '{nombre}'"}

# Controlador
class Controller:
    def __init__(self):
        self.route = APIRouter(prefix='/nombres')
        self.generalService = GeneralService()
        self._setup_routes()

    def _setup_routes(self):
        self.route.add_api_route("/obtener", self.obtener_nombres, methods=["GET"])
        self.route.add_api_route("/agregar", self.agregar_nombre, methods=["POST"])
        self.route.add_api_route("/actualizar", self.actualizar_nombre, methods=["PUT"])
        self.route.add_api_route("/borrar/{nombre}", self.borrar_nombre, methods=["DELETE"])

    # Endpoints
    async def obtener_nombres(self):
        return self.generalService.obtener_nombres()

    async def agregar_nombre(self, nombre: Nombre):
        return self.generalService.agregar_nombre(nombre.nombre)

    async def actualizar_nombre(self, update_data: UpdateNombre = Body(...)):
        return self.generalService.actualizar_nombre(update_data.nombreActual, update_data.nuevoNombre)

    async def borrar_nombre(self, nombre: str = Path(...)):
        return self.generalService.borrar_nombre(nombre)

# Registrar las rutas en la aplicación FastAPI
controller = Controller()
app.include_router(controller.route)

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI with MongoDB"}
