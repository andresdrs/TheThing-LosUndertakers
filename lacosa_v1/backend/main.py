from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configuración de CORS para permitir todas las solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiar "*" a la URL de tu frontend si está en un dominio específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(BaseModel):
    title: str


tasks = [] #donde almacenaré las tasks

@app.get("/tasks/") #si me llega get, muestro las tasks
def read_tasks():
    return tasks

@app.post("/tasks/") #si me llega post, agrego una nueva task a la lista
def create_task(task: Task):
    tasks.append(task)
    return task
