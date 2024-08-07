#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from os import getenv
from models.review import Review
from sqlalchemy import Table
from models.amenity import Amenity


if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float)
        longitude = Column(Float)
        amenity_ids = []
        reviews = relationship("Review", backref="place",
                               cascade="all, delete, delete-orphan")
        amenities = relationship("Amenity", secondary="place_amenity",
                                 viewonly=False)
    else:
        name = ''
        city_id = ''
        description = ''
        user_id = ''
        number_bathrooms = 0
        max_guest = 0
        number_rooms = 0
        price_by_night = 0
        longitude = 0.0
        latitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """ getter attribute returns the list of Review instances """
            from models import storage
            review_list = []
            for key, value in storage.all(Review).items():
                if value.place_id == self.id:
                    review_list.append(value)
            return review_list

        @property
        def amenity(self):
            """ getter attribute returns the list of Amenity instances """
            from models import storage
            amenity_list = []
            for key, value in storage.all(Amenity).items():
                if value.place_id == self.id:
                    amenity_list.append(value)
            return amenity_list

        @amenity.setter
        def amenity(self, obj):
            """ setter attribute handles append method for adding an Amenity.id
            to the attribute amenity_ids """
            if type(obj) == Amenity:
                self.amenity_ids.append(obj.id)
