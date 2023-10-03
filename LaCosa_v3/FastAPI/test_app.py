import pytest
from fastapi.testclient import TestClient
from main import app  # importamos la app de nuestro back

# Las fixtures son como datos que vamos a usar en los tests, son reutilizables.

# Una fixture para poder reusar el cliente en varios tests
@pytest.fixture
def client():
    return TestClient(app)

# fixture para la creación de un usuario user_one
@pytest.fixture
def sample_user_data_one():
    return {"nickname": "user_one"}

# fixture para la creación de un usuario user_two
@pytest.fixture
def sample_user_data_two():
    return {"nickname": "user_two"}

# Una fixture que tiene la configuración necesaria de una partida para testear la creación de partida
@pytest.fixture
def sample_game_data_one():
    return {
        "game_name": "test_game",
        "min_players": 2,
        "max_players": 5,
        "id_creator": 1
    }

# fixture para creación de partida tal que de error, ya que tiene el mismo nombre que la game_data_one
@pytest.fixture
def sample_game_data_two():
    return {
        "game_name": "test_game",
        "min_players": 3,
        "max_players": 5,
        "id_creator": 2
    }

# Esta fixture depende de sample_user_data_one,
# asegurando que el usuario user_one se crea antes que user_two
@pytest.fixture
def sample_user_one_created(client, sample_user_data_one):
    response = client.post("/users/", json=sample_user_data_one)
    assert response.status_code == 200
    return response.json()

# Esta fixture depende de sample_user_one_created,
# asegurando que el usuario user_two se crea después de user_one
@pytest.fixture
def sample_user_two_created(client, sample_user_data_two, sample_user_one_created):
    response = client.post("/users/", json=sample_user_data_two)
    assert response.status_code == 200
    return response.json()

def test_all(client, sample_user_one_created, sample_user_two_created, sample_game_data_one, sample_game_data_two):
    # user_data_one crea partida con datos game_data_one, debería ser exitoso con código 200
    response = client.post("/games/", json=sample_game_data_one)
    assert response.status_code == 200
    assert "game_name" in response.json()

    # user_data_two crea partida con datos game_data_two, debería dar bad request 
    # ya que no puede haber dos juegos con el mismo nombre
    response = client.post("/games/", json=sample_game_data_two)
    assert response.status_code == 400

    # Test para obtener lista de partidas, debería dar exitoso
    response = client.get("/games_list/")
    assert response.status_code == 200
    games = response.json()
    assert isinstance(games, list)  # Verificamos que games sea una lista de juegos

    # Test para unirse a una partida existente
    # El jugador con id 1 que creó su propia partida se une con éxito
    game_name = sample_game_data_one["game_name"]
    join_response_one = client.post(f"/games/{game_name}/join/1")
    assert join_response_one.status_code == 200

    # El jugador con id 2 que no está en una partida se une con éxito
    join_response_two = client.post(f"/games/{game_name}/join/2")
    assert join_response_two.status_code == 200

    # Test para tener la lista de jugadores en la única partida creada, éxito
    players_response = client.get(f"/games/{game_name}/players")
    assert players_response.status_code == 200
    players = players_response.json()
    assert isinstance(players, list)  # Verificamos que players sea una lista de jugadores

    # Test para iniciar una partida
    # usuario no creador intenta iniciar la partida, debería dar un código 400 (Bad Request)
    start_response = client.post(f"/games/{game_name}/start/2")
    assert start_response.status_code == 400

    # usuario creador intenta iniciar la partida, debería ser exitoso
    start_response = client.post(f"/games/{game_name}/start/1")
    assert start_response.status_code == 200


# Este test necesita tener instalado pytest: pip install pytest httpx
# y se ejecuta abriendo una terminal en el directorio donde está este archivo (test_app.py)
# y ejecutando: pytest.

# Tener en cuenta antes de ejecutar de reiniciar BD. Debe estar limpia sin datos antes de testear.
