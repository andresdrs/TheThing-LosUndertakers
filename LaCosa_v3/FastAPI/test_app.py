import pytest
from fastapi.testclient import TestClient
from main import app  # importamos la app de nuestro back

# las fixtures son como datos que vamos a usar en los tests, son reutilizables.

# una fixture para poder reusar el cliente en varios tests
@pytest.fixture
def client():
    return TestClient(app)

# una fixture que tiene un nickname para testear la creación de usuario
@pytest.fixture
def sample_user_data_one():
    return {"nickname": "user_one"}

@pytest.fixture
def sample_user_data_two():
    return {"nickname": "user_two"}

# una fixture que tiene la configuración necesaria de una partida para testear la creación de partida
@pytest.fixture
def sample_game_data_one():
    return {
        "game_name": "test_game",
        "min_players": 3,
        "max_players": 5,
        "id_creator": 1
    }

@pytest.fixture
def sample_game_data_two():
    return {
        "game_name": "test_game",
        "min_players": 3,
        "max_players": 5,
        "id_creator": 2
    }

# este test crea un usuario con user_data_one, debería ser exitoso con código 200
def test_create_user_ok(client, sample_user_data_one):
    response = client.post("/users/", json=sample_user_data_one)
    assert response.status_code == 200
    assert "user_id" in response.json()

# este test crea un usuario con user_data_two, debería ser exitoso con código 200
def test_create_user_ok(client, sample_user_data_two):
    response = client.post("/users/", json=sample_user_data_two)
    assert response.status_code == 200
    assert "user_id" in response.json()

# user_data_one crea partida con datos game_data_one, debería ser exitoso con código 200
def test_create_game_ok(client, sample_game_data_one):
    response = client.post("/games/", json=sample_game_data_one)
    assert response.status_code == 200
    assert "game_name" in response.json()

# user_data_two crea partida con datos game_data_two, debería dar bad request 
# ya que no puede haber dos juegos con el mismo nombre
def test_create_game_bad(client, sample_game_data_two):
    response = client.post("/games/", json=sample_game_data_two)
    assert response.status_code == 400

# este test necesita tener instalado pytest: pip install pytest httpx
# y se ejecuta abriendo una terminal en el directorio donde esta este archivo (test_app.py)
# y ejecutando: pytest.

# tener en cuenta antes de ejecutar de reiniciar BD. Debe estar limpia sin datos antes de testear.




