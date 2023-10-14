#!/usr/bin/python3
"""Unittest imports necessary modules"""
import unittest
import json
import os
from shutil import copy2

from models.state import State
from models import storage


class TestState(unittest.TestCase):
    """creates state class instance and checks to see whether it is instance.

    Attributes:
        __objects_backup (dict): copy of dictionary of `FileStorage` objects
        json_file (str): filename of JSON file containing `FileStorage` objects
        json_file_backup (str): backup filename for `json_file`

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
        """Cleanup required based on the test technique.
        """
        try:
            del (s1, s2)
        except NameError:
            pass
        storage._FileStorage__objects = dict()
        if os.path.exists(type(self).json_file):
            os.remove(type(self).json_file)

    def test_State(self):
        """Class and determines whether it is an instance
        """
        # No arguments are required for normal use.
        s1 = State()
        self.assertIsInstance(s1, State)

        # Attribute `name` is set to empty string by default.
        self.assertIsInstance(s1.name, str)
        self.assertEqual(s1.name, '')

        # FileStorage may serialize state to JSON.
        s1.name = 'test'
        self.assertIn(s1, storage._FileStorage__objects.values())
        s1.save()
        with open(storage._FileStorage__file_path, encoding='utf-8') as file:
            content = file.read()
        key = s1.__class__.__name__ + '.' + s1.id
        self.assertIn(key, json.loads(content))

        # FileStorage can deserialize state from JSON.
        self.assertIn(key, storage._FileStorage__objects.keys())
        storage._FileStorage__objects = dict()
        storage.reload()
        self.assertIn(key, storage._FileStorage__objects.keys())
