
from typing import Dict, Any
from enum import Enum

class estatus(Enum):
	lobby = 'lobby'
	inGame = 'inGame'
	finalizada = 'finalizada'


	


PARTIDAS = [
	{
		"Nombre": "juego_henrique",
		"min_jugadores": 5,
		"max_jugadores": 9,
		"is_started": True,
		"Jugadores": ["henrique", "rodolfo", "juan domingo"]
	},
	{
		"Nombre": "juego_ricardo",
		"min_jugadores": 4,
		"max_jugadores": 11,
		"is_started": False,
		"Jugadores": ["henrique", "rodolfo", "juan domingo"]
	},
	{
		"Nombre": "juego_pedrito",
		"min_jugadores": 8,
		"max_jugadores": 9,
		"is_started": True,
		"Jugadores": ["henrique", "rodolfo", "juan domingo"]
	},

]

def get_partida_by_name(game_name: str) -> Dict[str, Any]:
    res_game = None
    for game in PARTIDAS:
        if game["Nombre"] == game_name:
            res_game = game
            break
    return res_game