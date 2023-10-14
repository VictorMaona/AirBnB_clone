#!/usr/bin/python3
"""Unittest handles a variety of attributes and data"""
import unittest
import json
import os
from shutil import copy2

from models.place import Place
from models import storage


class TestPlace(unittest.TestCase):
    """Tests elements of the Place class such as default values of attributes.

    Attributes:
        __objects_backup (dict): copy of current dict of `FileStorage` objects
        json_file (str): filename for JSON file of `FileStorage` objects
        json_file_backup (str): filename for backup of `json_file`

    """
    __objects_backup = storage._FileStorage__objects
    json_file = storage._FileStorage__file_path
    json_file_backup = storage._FileStorage__file_path + '.bup'

    @classmethod
    def setUpClass(cls):
        """Configuration for all tests in the module.
        """
        storage._FileStorage__objects = dict()
        if os.path.exists(cls.json_file):
            copy2(cls.json_file, cls.json_file_backup)
            os.remove(cls.json_file)

    @classmethod
    def tearDownClass(cls):
        """After all module tests teardown.
        """
        storage._FileStorage__objects = cls.__objects_backup
        if os.path.exists(cls.json_file_backup):
            copy2(cls.json_file_backup, cls.json_file)
            os.remove(cls.json_file_backup)

    def tearDown(self):
        """Cleanup required per test method.
        """
        try:
            del (p1, p2)
        except NameError:
            pass
        storage._FileStorage__objects = dict()
        if os.path.exists(type(self).json_file):
            os.remove(type(self).json_file)

    def test_Place(self):
        """Various elements such as default values of attributes are tested.
        """
        # No arguments are required for normal use.
        p1 = Place()
        self.assertIsInstance(p1, Place)

        # The `city_id` attribute defaults to an empty string.
        self.assertIsInstance(p1.city_id, str)
        self.assertEqual(p1.city_id, '')

        # The `city_id` attribute defaults an empty string.
        self.assertIsInstance(p1.user_id, str)
        self.assertEqual(p1.user_id, '')

        #The attribute `name` is set to empty string by default.
        self.assertIsInstance(p1.name, str)
        self.assertEqual(p1.name, '')

        # Attribute `description` is set to empty string by default.
        self.assertIsInstance(p1.description, str)
        self.assertEqual(p1.description, '')

        # The default value for the attr `number_rooms` is int 0.
        self.assertIsInstance(p1.number_rooms, int)
        self.assertEqual(p1.number_rooms, 0)

        # The default value for the `number_bathrooms` is int 0
        self.assertIsInstance(p1.number_bathrooms, int)
        self.assertEqual(p1.number_bathrooms, 0)

        # The default value for the `max_guest` is int 0
        self.assertIsInstance(p1.max_guest, int)
        self.assertEqual(p1.max_guest, 0)

        # The default value for the `price_by_night` int 0
        self.assertIsInstance(p1.price_by_night, int)
        self.assertEqual(p1.price_by_night, 0)

        # The default value for the `latitude` to float 0.0
        self.assertIsInstance(p1.latitude, float)
        self.assertEqual(p1.latitude, 0.0)

        # The default value for the `longitude` to float 0.0
        self.assertIsInstance(p1.longitude, float)
        self.assertEqual(p1.longitude, 0.0)

        # The default value for the `amenity_ids` to empty list
        self.assertIsInstance(p1.amenity_ids, list)
        self.assertEqual(p1.amenity_ids, [])

        # FileStorage may serialize Place to JSON.
        p1.city_id = 'test1'
        p1.user_id = 'test2'
        p1.name = 'test3'
        p1.description = 'test4'
        p1.number_rooms = 1
        p1.number_bathrooms = -2
        p1.max_guest = 3
        p1.price_by_night = -4
        p1.latitude = -5.5
        p1.longitude = 6.6
        p1.amenity_ids = ['id1', 'id2']
        self.assertIn(p1, storage._FileStorage__objects.values())
        p1.save()
        with open(storage._FileStorage__file_path, encoding='utf-8') as file:
            content = file.read()
        key = p1.__class__.__name__ + '.' + p1.id
        self.assertIn(key, json.loads(content))

        # FileStorage can deserialize Place from JSON.
        self.assertIn(key, storage._FileStorage__objects.keys())
        storage._FileStorage__objects = dict()
        storage.reload()
        self.assertIn(key, storage._FileStorage__objects.keys())
