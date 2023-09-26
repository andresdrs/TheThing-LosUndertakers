# Va a tener todas las conexiones string que nos permitirán
# a su vez establecer conexión con MySQL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = 'mysql+pymysql://admin:admin@localhost:3306/TheThing_undertakers' # esta es la url a mi localhost

engine = create_engine(URL_DATABASE) # crea un motor de bd que sirve de conexión
                                     # nuestra BD será URL_DATABASE
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # necesario para trabajar con sqlalchemy

Base = declarative_base() # lo vamos a usar para declarar clases en sqlachemy