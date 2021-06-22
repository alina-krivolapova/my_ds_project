from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from connection_settings import db_connection_path

# connection to db
engine = create_engine(f'sqlite:////{db_connection_path}')
# create session
db_session = scoped_session(sessionmaker(bind=engine))

# base class to create table objects
Base = declarative_base()
# query binding
Base.query = db_session.query_property()
