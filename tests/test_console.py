#!/usr/bin/python3
"""class function runs once before all of the class tests"""
import unittest
import json
import os
from shutil import copy2
import cmd

from console import HBNBCommand
from models import storage


class TestConsole(unittest.TestCase):
    """The console command interpreter is put to the test.

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
        """Configurations for all tests in the module.
        """
        storage._FileStorage__objects = dict()
        if os.path.exists(cls.json_file):
            copy2(cls.json_file, cls.json_file_backup)
            os.remove(cls.json_file)

    @classmethod
    def tearDownClass(cls):
        """Dismantle after all module testing has been completed.
        """
        storage._FileStorage__objects = cls.__objects_backup
        if os.path.exists(cls.json_file_backup):
            copy2(cls.json_file_backup, cls.json_file)
            os.remove(cls.json_file_backup)

    def tearDown(self):
        """Any cleanup required in accordance with test method.
        """
        try:
            del (s1, s2)
        except NameError:
            pass
        storage._FileStorage__objects = dict()
        if os.path.exists(type(self).json_file):
            os.remove(type(self).json_file)

    def test_Console(self):
        """Console command interpreter is put to the test.
        """
        self.assertIsNotNone(HBNBCommand())
