#!/usr/bin/python3
"""Acts as a foundation for other classes"""
from . import storage
from datetime import datetime
import uuid


class BaseModel():
    """Methods for `BaseModel` and its subclasses.

    Attributes:
        id (str): UUID assigned when an instance is created
        created_at (datetime.datetime): instance is created, the current date and time
            is created
        updated_at (datetime.datetime): instance is created the current datetime
            is created updated whenever an object is altered

    """
    def __init__(self, *args, **kwargs):
        """Constructor for the `BaseModel` class.

        Project tasks:
            three. Is for BaseModel
            four. Make a BaseModel from a dictionary.

        """
        if kwargs is None or len(kwargs) == 0:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        else:
            ISO_fmt = '%Y-%m-%dT%H:%M:%S.%f'
            self.created_at = datetime.strptime(kwargs['created_at'], ISO_fmt)
            self.updated_at = datetime.strptime(kwargs['updated_at'], ISO_fmt)
            for key, value in kwargs.items():
                if key not in ('created_at', 'updated_at', '__class__'):
                    self.__dict__[key] = value

    def __str__(self):
        """The string representation of BaseModel is returned.

        Returns:
             '[<class name>] (<self.id>) <self.__dict__>'

        Project tasks:
            Three. Is for BaseModel

        """
        return "[{}] ({}) {}".format(
                self.__class__.__name__, self.id, str(self.__dict__))

    def save(self):
        """Updates updated_at with current datetime and saves changes to JSON
        serialization.

        Project tasks:
            Three. Is for BaseModel
            Five. Stores first object

        """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns dictionary contains all values of __dict__
        of instance, plus `__class__`, `created-at`, and `updated_at`.

        Project tasks:
            Three. Is for BaseModel

        """
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = self.__class__.__name__
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        return my_dict
