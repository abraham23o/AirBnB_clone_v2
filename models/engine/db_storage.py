#!/usr/bin/python3
"""New engine DBStorage"""
from os import getenv
from sqlalchemy import create_engine
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from models import city, amenity, state, review, user, place


class DBStorage:
    """This class manages storage of hbnb models in MySQL Relational DB"""
    __engine = None
    __session = None

    def __init__(self):
        """instantiate new db storage instance"""
        usr = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format
                                      (usr, password,
                                       host, database), pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        query on the current database session (self.__session) all objects
        depending on the class name (argument cls)
        """
        my_dict = {}
        classes = [user.User, state.State, city.City,
                   place.Place, review.Review, amenity.Amenity]

        if cls:
            classes = [cls]

        for i in classes:
            my_query = self.__session.query(cls).all()
            for obj in my_query:
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                my_dict[key] = i

        return my_dict

    def new(self, obj):
        """adds the object to the current database session (self.__session)"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database """
        Base.metadata.create_all(bind=self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """closes the working SQLAlchemy session"""
        self.__session.close()
