#!/usr/bin/env python3
'''
classes:
DBStorage: manage databases
'''
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    '''Class to create a engine for a mysql.'''

    __engine = None
    __session = None

    def __init__(self):
        '''Initialize the Enviroment variables.'''
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv("HBNB_MYSQL_USER"),
            getenv("HBNB_MYSQL_PWD"),
            getenv("HBNB_MYSQL_HOST"),
            getenv("HBNB_MYSQL_DB")), pool_pre_ping=True)

        if getenv("HBNB_ENV") == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):

        if cls:
            objects = self.__session.query(cls).all()
        else:
            classes = [State, City, User, Place, Review, Amenity]
            objects = []
            for c in classes:
                objects += self.__session.query(c)
        dicty = {}
        for obj in objects:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            dicty[key] = obj
        return dicty

    def new(self, obj):
        '''Add the object to the current database session.'''
        if obj:
            self.__session.add(obj)

    def save(self):
        '''Commit all changes of the current database session.'''
        self.__session.commit()

    def delete(self, obj=None):
        '''Delete from the current database session obj.'''
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """ session close
        """

        self.__session.close()
