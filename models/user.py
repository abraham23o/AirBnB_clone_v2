#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
import os
from sqlalchemy.orm import relationship


if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    class User(BaseModel, Base):
        """This class defines a user by various attributes"""
        __tablename__ = 'users'

        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        places = relationship("Place",
                              cascade="all, delete-orphan", backref="user")

else:
    class User(BaseModel):
        """This class defines a user by various attributes"""
        __tablename__ = 'users'

        email = ""
        password = ""
        first_name = ""
        last_name = ""
