#!/usr/bin/python3
"""used to load these objects from the JSON file back into memory"""
import json
from os import path


class FileStorage():
    """Responsible for managing JSON file storage for the `BaseModel` class.

    Attributes:
        __file_path (str): default for saving JSON serializations file
        __objects (dict): dict of `BaseModel` objects and child classes
            as values, and '<object class name>.<object.id>' as keys

    Project tasks:
        5. Store first object

    """
    __file_path = 'HBnB_objects.json'
    __objects = dict()

    def __init__(self):
        pass

    def all(self):
        """The dictionary items are returned__objects.

        Returns:
            __objects (dict): dict items with `BaseModel` and child
                classes as values, and '<object class name>.<object.id>' as
                keys

        Project tasks:
            5. Store first object

        """
        return self.__objects

    def new(self, obj):
        """Sets new object in __objects with key value.
        '<object class name>.<object.id>'

        Args:
            obj (BaseModel or child): BaseModel-derived object to be added to
               __objects

        Project tasks:
            5. Store first object

        """
        self.__objects[obj.__class__.__name__ + '.' + obj.id] = obj

    def save(self):
        """__objects are serialized to the JSON file path: __file_path

        Project tasks:
           5. Store first object

        """
        json_dict = dict()
        for key, value in self.__objects.items():
            json_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(json_dict))

    def reload(self):
        """deserializes the JSON file at __file_path into __objects.
        exists; otherwise, there are no exceptions.

        Project tasks:
            5. Store first object

        """
        from ..base_model import BaseModel
        from ..user import User
        from ..state import State
        from ..city import City
        from ..amenity import Amenity
        from ..place import Place
        from ..review import Review

        classes = [BaseModel, User, State, City, Amenity, Place, Review]
        class_dict = dict()
        for c in classes:
            class_dict[c.__name__] = c

        if path.exists(self.__file_path) is True:
            with open(self.__file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if content is not None and content != '':
                    json_dict = json.loads(content)
                    for key, value in json_dict.items():
                        obj_class = class_dict[value['__class__']]
                        self.__objects[key] = obj_class(**value)
        else:
            pass
