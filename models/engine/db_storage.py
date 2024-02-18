#!/usr/bin/python3
""" DBStorage module for HBNB project """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ DBStorage class """
    __engine = None
    __session = None

    def __init__(self):
        """ Initializes DBStorage """
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST", default="localhost")
        database = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV", default="")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                      .format(user, password, host, database),
                                      pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)
        else:
            Base.metadata.create_all(self.__engine)
    def all(self, cls=None):
        """Query on the current database session"""
        objects = {}
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
                objs = self.__session.query(cls).all()
        else:
            state_objs = self.__session.query(State).all()
            city_objs = self.__session.query(City).all()
            objs = state_objs + city_objs
        for obj in objs:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            objects[key] = obj
        return objects

    def new(self, obj):
        """ Add the object to the current database session """
        obj.id = str(obj.id)
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session obj if not None """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database and create session """
        from models import base_model
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine,
                expire_on_commit=False
                )
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ Close the current session """
        self.__session.remove()

    def get_engine(self):
        return self.__engine

    def get_session(self):
        return self.__session

    def close(self):
        """Closes the current session."""
        self.__session.remove()
