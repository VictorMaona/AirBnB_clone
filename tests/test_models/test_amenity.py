#!/usr/bin/python3
"""Puts several facets of Amenity class behavior to the test."""
import unittest
import json
import os
from shutil import copy2

from models.amenity import Amenity
from models import storage


class TestAmenity(unittest.TestCase):
    """ `Amenity` lesson is put to the test.
    test_base_model for interactions with args and kwargs.

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
        """This class method is used to initialize the test conditions.
        """
        storage._FileStorage__objects = dict()
        if os.path.exists(cls.json_file):
            copy2(cls.json_file, cls.json_file_backup)
            os.remove(cls.json_file)

    @classmethod
    def tearDownClass(cls):
        """This class function is used to clean up all tests in class.
        """
        storage._FileStorage__objects = cls.__objects_backup
        if os.path.exists(cls.json_file_backup):
            copy2(cls.json_file_backup, cls.json_file)
            os.remove(cls.json_file_backup)

    def tearDown(self):
        """Function is run after each test method to clean up leftovers.
        """
        try:
            del (a1, a2)
        except NameError:
            pass
        storage._FileStorage__objects = dict()
        if os.path.exists(type(self).json_file):
            os.remove(type(self).json_file)

    def test_Amenity(self):
        """Test case includes various assertions to validate the behavior.
        """
        # No arguments are required for normal use.
        a1 = Amenity()
        self.assertIsInstance(a1, Amenity)

        # The attribute `name` is set to the empty string by default.
        self.assertIsInstance(a1.name, str)
        self.assertEqual(a1.name, '')

        # FileStorage may serialize Amenity to JSON.
        a1.name = 'test'
        self.assertIn(a1, storage._FileStorage__objects.values())
        a1.save()
        with open(storage._FileStorage__file_path, encoding='utf-8') as file:
            content = file.read()
        key = a1.__class__.__name__ + '.' + a1.id
        self.assertIn(key, json.loads(content))

        # FileStorage may deserialize Amenity from JSON.
        self.assertIn(key, storage._FileStorage__objects.keys())
        storage._FileStorage__objects = dict()
        storage.reload()
        self.assertIn(key, storage._FileStorage__objects.keys())
