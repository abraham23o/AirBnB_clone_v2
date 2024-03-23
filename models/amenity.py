#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import os
from sqlalchemy import Column, String

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    class Amenity(BaseModel, Base):
        """Amenity class"""
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)

else:
    class Amenity(BaseModel):
        name = ""
