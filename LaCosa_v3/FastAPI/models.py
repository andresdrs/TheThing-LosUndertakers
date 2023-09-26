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
    user_game = Column(Integer) 

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, index=True)
    game_name = Column(String(50), unique=False)
    game_state = (Integer) # podemos definir a los estados como enteros (0 no inciada, 1 iniciada, 2 finalizada)
    min_players = Column(Integer)
    max_players = Column(Integer)
