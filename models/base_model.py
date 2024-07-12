#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models
from datetime import datetime
import uuid

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
                if 'id' not in kwargs:
                    self.id = str(uuid.uuid4())
                if 'created_at' not in kwargs:
                    self.created_at = datetime.now()
                if 'created_at' in kwargs and 'updated_at' not in kwargs:
                    self.updated_at = self.created_at
                else:
                    self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = dict(self.__dict__)
        dictionary["__class__"] = str(type(self).__name__)
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        if dictionary.__contains__('_sa_instance_state'):
            dictionary.pop('_sa_instance_state')

        return dictionary

    def delete(self):
        """
        deletes the current instance from the storage
        """
        models.storage.delete(self)
