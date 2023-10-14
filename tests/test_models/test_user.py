#!/usr/bin/python3
"""Unittest `User` class can be created saved and loaded from JSON"""
import unittest
import json
import os
from shutil import copy2

from models.user import User
from models import storage


class TestUser(unittest.TestCase):
    """method is a `User` class test case..

    Attributes:
        __objects_backup (dict): current dict of `FileStorage` objects
        json_file (str): filename for a JSON file of `FileStorage` objects
        json_file_backup (str): filename for a backup of `json_file`

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
            del (u1, u2)
        except NameError:
            pass
        storage._FileStorage__objects = dict()
        if os.path.exists(type(self).json_file):
            os.remove(type(self).json_file)

    def test_User(self):
        """Defines the `TestUser` test class which derives from .
        """
        # testTestUser There are no arguments in normal use. 
        u1 = User()
        self.assertIsInstance(u1, User)

        # attribute `email` is set to the empty string by default.
        self.assertIsInstance(u1.email, str)
        self.assertEqual(u1.email, '')

        # default value for attr 'password' is empty string.
        self.assertIsInstance(u1.password, str)
        self.assertEqual(u1.password, '')

        # attr `first_name` is set to an empty string by default.
        self.assertIsInstance(u1.first_name, str)
        self.assertEqual(u1.first_name, '')

        # attr `last_name` is set to an empty string by default.
        self.assertIsInstance(u1.last_name, str)
        self.assertEqual(u1.last_name, '')

        # FileStorage may serialize a user to JSON.
        u1.email = 'test1'
        u1.password = 'test2'
        u1.first_name = 'test3'
        u1.last_name = 'test4'
        self.assertIn(u1, storage._FileStorage__objects.values())
        u1.save()
        with open(storage._FileStorage__file_path, encoding='utf-8') as file:
            content = file.read()
        key = u1.__class__.__name__ + '.' + u1.id
        self.assertIn(key, json.loads(content))

        # FileStorage can deserialize user from JSON.
        self.assertIn(key, storage._FileStorage__objects.keys())
        storage._FileStorage__objects = dict()
        storage.reload()
        self.assertIn(key, storage._FileStorage__objects.keys())
