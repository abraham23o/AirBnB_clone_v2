#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
import os

if os.getenv('HBNB_TYPE_STORAGE') == 'db':

    class State(BaseModel, Base):
        """ State class """
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)

        cities = relationship("City",
                              backref='state',
                              cascade='all, delete-orphan')
else:
    class State(BaseModel):
        """Attributes:
                    name (str): The name of the state.
                    """

        name = ""

    @property
    def cities(self):
        """getter attribute cities that returns the list of City"""
        from models import storage
        my_list = []
        my_cities = storage.all(City).values()
        for city in my_cities:
            if self.id == city.state_id:
                my_list.append(city)
        return my_list
