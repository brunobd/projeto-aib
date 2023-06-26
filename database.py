from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from configparser import ConfigParser

file = "database.ini"
config = ConfigParser()
config.read(file)
user = config["database"]["user"]
host = config["database"]["host"]
password = config["database"]["password"]
port = config["database"]["port"]
db = config["database"]["db"]

DB_URL = "postgresql://{user}:{password}@{host}:{port}/{db}".format(
    user=user, password=password, host=host, port=port, db=db
)

engine = create_engine(DB_URL)
sessionlocal = sessionmaker(bind=engine)
Base = declarative_base()
