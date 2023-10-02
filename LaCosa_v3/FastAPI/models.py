# lo que sqlachemy usa para crear las tablas en mysql
from sqlalchemy import Boolean, Column, Integer, String
from database import Base

# nuestra app primero nos permitirá generar un usuario
# y crear partidas. Definiremos aquí las respectivas tablas.

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50), unique = True ) # largo es 50
    is_creator = Column(Boolean)
    user_game = Column(String(50)) 

class Game(Base):
    __tablename__ = 'games'

    game_name = Column(String(50), primary_key=True) # no tenemos id de game, el id será el nombre. No puede haber dos partidas con el mismo nombre
    game_state = Column(Integer) # podemos definir a los estados como enteros (0 no inciada, 1 iniciada, 2 finalizada)
    players_in = Column(Integer)
    min_players = Column(Integer)
    max_players = Column(Integer)
    id_creator = Column(Integer)
