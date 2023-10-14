#!/usr/bin/python3
"""Validate the functionality of the Review class and its interactions.""
import unittest
import json
import os
from shutil import copy2

from models.review import Review
from models import storage


class TestReview(unittest.TestCase):
    """method is a Review class test case.

    Attributes:
        __objects_backup (dict): current dict of `FileStorage` bjects copied
        json_file (str): filename of a JSON file containing `FileStorage` objects
        json_file_backup (str): backup filename for `json_file`

    """
    __objects_backup = storage._FileStorage__objects
    json_file = storage._FileStorage__file_path
    json_file_backup = storage._FileStorage__file_path + '.bup'

    @classmethod
    def setUpClass(cls):
        """Setup for all tests in module.
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
            del (r1, r2)
        except NameError:
            pass
        storage._FileStorage__objects = dict()
        if os.path.exists(type(self).json_file):
            os.remove(type(self).json_file)

    def test_Review(self):
        """Generates instance of Review class and tests it.
        """
        # No arguments required for normal use.
        r1 = Review()
        self.assertIsInstance(r1, Review)

        # Is `place_id` is set to empty string by default.
        self.assertIsInstance(r1.place_id, str)
        self.assertEqual(r1.place_id, '')

        # Attribute `user_id` is set an empty string by default.
        self.assertIsInstance(r1.user_id, str)
        self.assertEqual(r1.user_id, '')

        # Default value for attr `text` is an empty string.
        self.assertIsInstance(r1.text, str)
        self.assertEqual(r1.text, '')

        # FileStorage may serialize reviews to JSON.
        r1.place_id = 'test'
        r1.user_id = 'test'
        r1.text = 'test'
        self.assertIn(r1, storage._FileStorage__objects.values())
        r1.save()
        with open(storage._FileStorage__file_path, encoding='utf-8') as file:
            content = file.read()
        key = r1.__class__.__name__ + '.' + r1.id
        self.assertIn(key, json.loads(content))

        # FileStorage can deserialize Review from JSON.
        self.assertIn(key, storage._FileStorage__objects.keys())
        storage._FileStorage__objects = dict()
        storage.reload()
        self.assertIn(key, storage._FileStorage__objects.keys())
