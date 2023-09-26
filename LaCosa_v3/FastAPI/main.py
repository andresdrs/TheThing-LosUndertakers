from fastapi import FastAPI, HTTPException, status, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models

# mecanismo de seguridad ante peticiones HTTP cruzadas de distintos orígenes
# restringe las peticiones a un recurso desde un origen diferente al del recurso
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuración de CORS para permitir todas las solicitudes desde cualquier origen
# la url que sale es la url del front end.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine) # creamos db automáticamente cuando se inicie fastapi app

# ahora definimos un modelo pydantic, que sirve para transformar
# datos de entrada a objetos de Python. O sea, lo que llegue
# de las requests, usa estos modelos para traducirse a objetos
# que manejamos en nuestro sistema.

class userBase(BaseModel): # lo que entra en petición (solo esto para creación de jugador)
    nickname : str

class gameBase(BaseModel):
    game_name : str
    min_players : int
    max_players : int

def get_db(): # se intenta conexión con db.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# definimos endpoints!!!

# creación de usuario
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: userBase, db : Session = Depends(get_db)): # lo de session es un parámetro opcional
    db_user = models.User(**user.dict()) # el input (user de tipo userBase) se traduce al tipo de dato que ya
                                         # definimos en models (User). Se usa dict para transformar user en algo más facil de traducir
   
    db.add(db_user) # se agrega a bd nuevo usuario
    db.commit() # se commitea el cambio en la bd


# creación de partida
@app.post("/games/", status_code=status.HTTP_201_CREATED)
async def create_user(game: gameBase, db : Session = Depends(get_db)):
    db_game = models.Game(**game.dict()) # el input (gameBase) se traduce al tipo de dato que ya
                                         # definimos en models (Game)
    db.add(db_game)
    db.commit()

# mostrar listado de partidas