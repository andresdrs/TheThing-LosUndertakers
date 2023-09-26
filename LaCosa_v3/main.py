
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from partidas import PARTIDAS, get_partida_by_name
from typing import Dict



app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware



# Configuración de CORS para permitir todas las solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todas las cabeceras
)


class Game(BaseModel):
    def __init__(self, name, max_players, min_players, is_started=False):
        self.name = name
        self.max_players = max_players
        self.min_players = min_players
        self.is_started = is_started
        self.players = []



@app.post("/create_game")
def create_game(game_data: dict):
    name = game_data.get('name')
    max_players = game_data.get('max_players')
    min_players = game_data.get('min_players')

    if not all([name, max_players, min_players]):
        raise HTTPException(status_code=422, detail="Invalid game data")

    game = Game(name, max_players, min_players)
    PARTIDAS.append(game)
    return game

@app.get("/games")
def get_games():
    return PARTIDAS

@app.post("/join_game")
def join_game(username: str, game_name: str):
    for game in games:
        if game.name == game_name and len(game.players) < game.max_players:
            game.players.append(username)
            return game
    return None

@app.get("/game_details/{game_name}")
def get_game_details(game_name: str):
    res_game = None
    res_game = get_partida_by_name(game_name=game_name)
    if not res_game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="game not found"
        )
    return res_game



