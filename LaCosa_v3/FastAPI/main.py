from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine
import models
from typing import List
from fastapi.responses import JSONResponse


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

class gameBase(BaseModel): # lo que entra en petición (solo esto para creación de partida)
    game_name : str
    min_players : int
    max_players : int
    id_creator : int

def get_db(): # se intenta conexión con db.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# definimos endpoints!!!

# creación de usuario
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: userBase, db: Session = Depends(get_db)):
    # verificar si ya hay un usuario con el mismo nombre
    existing_user = db.query(models.User).filter(models.User.nickname == user.nickname).first()
    # si se encuentra user con mismo nombre, se guarda en existing_user y salta excepción
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    # si no, continuamos...

    # Crear un nuevo usuario a partir de la información proporcionada en userBase
    db_user = models.User(**user.dict())

    # Agregar el usuario a la base de datos y confirmar la transacción
    db.add(db_user)
    db.commit()

    # Devolver una respuesta con el playerId (user.id) 
    # esto es porque tengo que pasa el user id a las otras páginas
    return JSONResponse(content={"user_id": db_user.id})


# versión joaquín adaptada
@app.post("/games/", status_code=status.HTTP_201_CREATED)
async def create_game(game: gameBase, db: Session = Depends(get_db)):
    # hacemos manejos de errores. Si ocurre algún error dentro del bloque try, salta excepción del final.
    try:
        # vemos si ya existe un juego con el nombre que queremos
        existing_game = db.query(models.Game).filter(models.Game.game_name == game.game_name).first()
        if existing_game:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Game with this name already exists.")
        # si existe, salta excepción, si no, continuamos ...

        # creamos juego con la info que vino de parámetro e inicializamos valores de game_state y players_in
        db_game = models.Game(**game.dict())
        db_game.game_state = 0
        db_game.players_in = 0

        # agregamos a database
        db.add(db_game)
        # actualizamos database
        db.commit()

        # acá hago que la instancia de mi base de datos (que es db_game)
        # este up to date con los últimos cambios
        db.refresh(db_game)

        # devuelvo el nombre del game para que se haga el joinGame después
        # porque el creador de la partida
        return {"game_name": db_game.game_name}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



# mostrar listado de partidas
# versión joaquín adaptada
@app.get("/games_list/", response_model=List[gameBase])
async def get_games(skip: int = 0, limit: int = 10, db : Session = Depends(get_db)):
    # joaquín había hecho la versión con listas que retornaba la lista de partidas pero
    # en este caso se devuelve una lista de objetos tipo Game que tengan el game_state en 0 (o sea partidas no iniciadas)

    # la lista es objeto de tipo List de la librería typing (ni idea)
    games = db.query(models.Game).filter(models.Game.game_state == 0).offset(skip).limit(limit).all()
    return games

# versión joaquín adaptada
@app.post("/games/{game_name}/join/{player_id}", status_code=status.HTTP_200_OK)
async def join_game(game_name: str, player_id: int, db: Session = Depends(get_db)):
    
    # busco el juego que tiene el nombre game_name (obtenido como parámetro) en mi BD
    game = db.query(models.Game).filter(models.Game.game_name == game_name).first()
    if not game: # si no existe el game, tiro excepción
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    
    # si el game esta lleno, tiro excepción
    # esto es adaptado del código de joaquín
    if game.players_in is not None and game.players_in >= game.max_players:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Game is already full")


    # chequeo que el usuario que se quiere unir al juego no esté
    # en otro juego ya.
    existing_player_game = db.query(models.User).filter(models.User.id == player_id).first()
    if existing_player_game and existing_player_game.user_game:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Player is already in a game")
    
    # busco el usuario que tiene el id player_id en mi BD
    # y le actualizo los atributos.
    # caso 1: el player_id es el que creó el juego
    if game.id_creator == player_id:
        user = db.query(models.User).filter(models.User.id == game.id_creator).first()
        if user:
            user.user_game = game.game_name #pongo que está en el juego con game_name
            user.is_creator = 1 #le pongo en 1 el atributo de creador
    else:
        # caso 2: se une un jugador que no es el creador
        user = db.query(models.User).filter(models.User.id == player_id).first()
        user.is_creator = 0 #creador en 0
        user.user_game = game_name #pongo que esta en el juego game_name

    # actualizo la cantidad de jugadores en el juego
    game.players_in += 1

    # actualizo bd
    db.commit()

    return {"message": "Te has unido a la partida."} # esto no se si es de ayuda pero bueno

# obtener listado de jugadores en el juego
@app.get("/games/{game_name}/players", response_model=List[userBase])
async def get_players_in_game(game_name: str, db: Session = Depends(get_db)):
    # Buscar la partida por su nombre
    game = db.query(models.Game).filter(models.Game.game_name == game_name).first()
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    
    # Obtener la lista de jugadores que están en la partida
    players = db.query(models.User).filter(models.User.user_game == game_name).all()
    return players

# iniciar partida
@app.post("/games/{game_name}/start/{player_id}", status_code=status.HTTP_200_OK)
async def start_game(game_name: str, player_id: int, db : Session = Depends(get_db)):
    # chequear que el juego existe
    game = db.query(models.Game).filter(models.Game.game_name == game_name).first()
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    
    # busco el user que tiene el player_id del jugador que mando la petición de iniciar partida
    user = db.query(models.User).filter(models.User.id == player_id).first()
    # solo el creador puede inicar partida, me fijo si el usuario obtenido es creador
    # tengamos en cuenta que solo basta ver si es creador, no hace falta ver si el nombre de la partida
    # de user_game es el mismo a game_name pasado en parámetro, ya que un jugador sólo puede estar
    # en una sola partida, y si un jugador es creador, está únicamente en la partida que creó, que es la de game_name
    if user.is_creator:
        # como se inicia el juego, se cambia el estado del juego inciado
        game.game_state = 1
        # Commit the changes to the database
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Player isn't creator")
    
    return {"message": "Game started successfully"}

# este endpoint lo uso para poder hacer que todos los jugadores en una partida vayan al juego cuando se inicia
@app.get("/games/{game_name}/status")
async def get_game_status(game_name: str, db: Session = Depends(get_db)):
    # obtengo el juego
    game = db.query(models.Game).filter(models.Game.game_name == game_name).first()
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")

    return {"gameStarted": game.game_state == 1} # si el juego esta iniciado, devuelve 1 (de iniciado)
