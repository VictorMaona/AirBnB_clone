#!/usr/bin/python3
"""Unit test validates the City class basic functionality and behavior."""
import unittest
import json
import os
from shutil import copy2

from models.city import City
from models import storage


class TestCity(unittest.TestCase):
    """Tests a `City` class.
    Test_base_model for interactions with args and kwargs.

    Attributes:
        __objects_backup (dict): copy current dict for `FileStorage` objects
        json_file (str): filename JSON file of `FileStorage` objects
        json_file_backup (str): filename for backup `json_file`

    """
    __objects_backup = storage._FileStorage__objects
    json_file = storage._FileStorage__file_path
    json_file_backup = storage._FileStorage__file_path + '.bup'

    @classmethod
    def setUpClass(cls):
        """Configuration for all tests in module.
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
        """Any necessary cleanup as determined by test procedure.
        """
        try:
            del (c1, c2)
        except NameError:
            pass
        storage._FileStorage__objects = dict()
        if os.path.exists(type(self).json_file):
            os.remove(type(self).json_file)

    def test_City(self):
        """Tests for the `City` class.
        """
        # No arguments required for normal use.
        c1 = City()
        self.assertIsInstance(c1, City)

        # The attribute `name` is set to the empty string by default.
        self.assertIsInstance(c1.name, str)
        self.assertEqual(c1.name, '')

        # The attribute `state_id` is set to an empty string by default.
        self.assertIsInstance(c1.state_id, str)
        self.assertEqual(c1.state_id, '')

        # FileStorage can serialize City to JSON.
        c1.name = 'test'
        c1.state_id = 'test'
        self.assertIn(c1, storage._FileStorage__objects.values())
        c1.save()
        with open(storage._FileStorage__file_path, encoding='utf-8') as file:
            content = file.read()
        key = c1.__class__.__name__ + '.' + c1.id
        self.assertIn(key, json.loads(content))

        # FileStorage can deserialize city from JSON.
        self.assertIn(key, storage._FileStorage__objects.keys())
        storage._FileStorage__objects = dict()
        storage.reload()
        self.assertIn(key, storage._FileStorage__objects.keys())
