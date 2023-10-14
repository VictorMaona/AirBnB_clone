#!/usr/bin/python3
"""Class unit test covers aspects of functionality and interactions."""
import datetime
import json
import os
import re
from shutil import copy2
import unittest

from models.base_model import BaseModel
from models import storage


def test_default_init(testobj, basemodel):
    # obj represents a BaseModel instance.
    testobj.assertIsInstance(basemodel, BaseModel)

    # obj was assigned with UUID, created_at and updated_at
    testobj.assertIsNotNone(basemodel.id)
    testobj.assertIsNotNone(basemodel.created_at)
    testobj.assertIsNotNone(basemodel.updated_at)


def test_default_id(testobj, basemodel):
    # The string id
    testobj.assertIs(type(basemodel.id), str)
    testobj.assertIsInstance(basemodel.id, str)

    # The id is in the uuid format.
    UUIDv4_regex = ('^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-'
                    '[89ab][a-f0-9]{3}-[a-f0-9]{12}$')
    UUIDv4 = re.compile(UUIDv4_regex, re.IGNORECASE)
    testobj.assertRegex(basemodel.id, UUIDv4)


def test_default_created_at(testobj, basemodel):
    # The datetime object created_at
    testobj.assertIs(type(basemodel.created_at), datetime.datetime)
    testobj.assertIsInstance(basemodel.created_at, datetime.datetime)

    # UTC created_at tzinfo = None
    testobj.assertIsNone(basemodel.created_at.tzinfo)

    # The new instance created_at matches the current time to the second.
    current = datetime.datetime.now()
    testobj.assertEqual(current.isoformat()[:-6],
                        basemodel.created_at.isoformat()[:-6])

    # created_at is a string that can be translated to ISO format.
    ISO_format = '%Y-%m-%dT%H:%M:%S.%f'
    dt_str = basemodel.created_at.strftime(ISO_format)
    testobj.assertEqual(dt_str, basemodel.created_at.isoformat())


def test_default_updated_at(testobj, basemodel):
    # Datetime object updated_at
    testobj.assertIs(type(basemodel.updated_at), datetime.datetime)
    testobj.assertIsInstance(basemodel.updated_at, datetime.datetime)

    # UTC updated_at tzinfo = None
    testobj.assertIsNone(basemodel.updated_at.tzinfo)

    # updated_at for new instance corresponds to current time to the second
    current = datetime.datetime.now()
    testobj.assertEqual(current.isoformat()[:-6],
                        basemodel.updated_at.isoformat()[:-6])

    # updated_at is a string that can be translated to ISO format.
    ISO_format = '%Y-%m-%dT%H:%M:%S.%f'
    dt_str = basemodel.updated_at.strftime(ISO_format)
    testobj.assertEqual(dt_str, basemodel.updated_at.isoformat())


class TestBaseModel(unittest.TestCase):
    """Test case includes assertions to validate the `BaseModel` behavior. 
    Attributes:
        __objects_backup (dict): copy of dict of `FileStorage` objects
        json_file (str): filename for JSON file `FileStorage` objects
        json_file_backup (str): filename backup of `json_file`
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
        """Teardown after all module tests have been completed.
        """
        storage._FileStorage__objects = cls.__objects_backup
        if os.path.exists(cls.json_file_backup):
            copy2(cls.json_file_backup, cls.json_file)
            os.remove(cls.json_file_backup)

    def tearDown(self):
        """Any necessary cleanup as determined by the test procedure.
        """
        try:
            del (bm1, bm2, bm3, bm4, bm5)
        except NameError:
            pass
        storage._FileStorage__objects = dict()
        if os.path.exists(type(self).json_file):
            os.remove(type(self).json_file)

    def test_BaseModel(self):
        """The class `BaseModel` is tested for instantiation and type.
        """
        # No arguments are required for normal use.
        bm1 = BaseModel()
        test_default_init(self, bm1)

        # only arg as an argument no kwarg
        bm2 = BaseModel(None)
        test_default_init(self, bm2)
        test_default_id(self, bm2)
        test_default_created_at(self, bm2)
        test_default_updated_at(self, bm2)

        # Both arg and kwarg are supplied as arguments.
        bm1_kwarg = bm1.to_dict()
        bm3 = BaseModel("Holberton", **bm1_kwarg)
        test_default_init(self, bm3)
        test_default_id(self, bm3)
        self.assertEqual(bm1.id, bm3.id)
        test_default_created_at(self, bm3)
        self.assertEqual(bm1.created_at, bm3.created_at)
        test_default_updated_at(self, bm3)
        self.assertEqual(bm1.updated_at, bm3.updated_at)

        # passing kwarg plus keys not in dict
        bm1.name = "My_First_Model"
        bm1.num = 89
        bm1_kwarg = bm1.to_dict()
        bm4 = BaseModel(**bm1_kwarg)
        test_default_init(self, bm4)
        self.assertIsNotNone(bm4.name)
        self.assertEqual(bm1.name, bm4.name)
        self.assertIsNotNone(bm4.num)
        self.assertEqual(bm1.num, bm4.num)
        test_default_id(self, bm4)
        self.assertEqual(bm1.id, bm4.id)
        test_default_created_at(self, bm4)
        self.assertEqual(bm1.created_at, bm4.created_at)
        test_default_updated_at(self, bm4)
        self.assertEqual(bm1.updated_at, bm4.updated_at)

        # As an argument use an empty dictionary.
        empty = {}
        bm5 = BaseModel(**empty)
        test_default_init(self, bm5)
        test_default_id(self, bm5)
        test_default_created_at(self, bm5)
        test_default_updated_at(self, bm5)

        # In BaseModel.__init__ storage.new() is called to add obj to __objects__.
        self.assertIn(bm1, storage._FileStorage__objects.values())

    def test_id(self):
        """The public instance attribute `id` is put to the test.
        """
        # Usage in the normal:
        bm1 = BaseModel()
        test_default_id(self, bm1)

        # Each instance has functionally unique id.
        bm2 = BaseModel()
        bm3 = BaseModel()
        self.assertNotEqual(bm1.id, bm2.id)
        self.assertNotEqual(bm2.id, bm3.id)

        # ID is public attribute that can be manually reassigned.
        bm1.id = bm2.id
        self.assertEqual(bm1.id, bm2.id)

        # Manual reassignment risks resulting in an incorrect UUID format.
        bm3.id = '1234567890'
        UUIDv4_regex = ('^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-'
                        '[89ab][a-f0-9]{3}-[a-f0-9]{12}$')
        self.assertIsNone(re.match(UUIDv4_regex, bm3.id, re.IGNORECASE))

    def test_created_at(self):
        """The public instance attribute `created_at` is put to the test.
        """
        # Usage of Normal:
        bm1 = BaseModel()
        test_default_created_at(self, bm1)

        # created_at is public attribute that can be reassigned manually.
        bm2 = BaseModel()
        bm1.created_at = bm2.created_at
        self.assertEqual(bm1.created_at, bm2.created_at)

        # Direct manual reassignment may result in an incorrect format.
        bm2.created_at = '1234567890'
        self.assertNotIsInstance(bm2.created_at, datetime.datetime)

    def test_updated_at(self):
        """The public instance attribute `updated_at` put to the test.
        """
        # No arguments are required for normal use.
        bm1 = BaseModel()
        test_default_updated_at(self, bm1)

        # updated_at is a public attribute that can be reassigned manually.
        bm2 = BaseModel()
        bm1.updated_at = bm2.updated_at
        self.assertEqual(bm1.updated_at, bm2.updated_at)

        # Direct manual reassignment may result in an incorrect format.
        bm2.updated_at = '1234567890'
        self.assertNotIsInstance(bm2.updated_at, datetime.datetime)

    def test___str__(self):
        """Private instance method `__str__` is tested.
        """
        # Usage of Normal:
        bm1 = BaseModel()

        # '[<class name>] (<self.id>) <self.__dict__>' prints.
        __str = str(bm1)
        self.assertEqual(__str, '[' + bm1.__class__.__name__ + '] (' +
                         bm1.id + ') ' + str(bm1.__dict__))

        # __str__ BaseModel without instantiation
        self.assertEqual(str(BaseModel),
                         "<class 'models.base_model.BaseModel'>")

    def test_save(self):
        """The public instance method `save` is put to the test.
        """
        # Usage of normal:
        bm1 = BaseModel()

        # updated_at begins at the same time as created_at.
        self.assertEqual(bm1.created_at.isoformat()[:-6],
                         bm1.updated_at.isoformat()[:-6])

        # updated_at is a public attribute that can be reassigned manually.
        ISO_format = '%Y-%m-%dT%H:%M:%S.%f'
        example_ISO = '1900-05-13T01:10:20.000001'
        dt_update = datetime.datetime.strptime(example_ISO, ISO_format)
        bm1.updated_at = dt_update
        self.assertNotEqual(bm1.created_at.year, bm1.updated_at.year)

        # save() changes value of updated_at to match current time to second.
        current = datetime.datetime.now()
        bm1.save()
        self.assertEqual(current.isoformat()[:-6],
                         bm1.updated_at.isoformat()[:-6])

        # updated_at is still in UTC tzinfo = None
        self.assertIsNone(bm1.updated_at.tzinfo)

        # updated_at can still be transformed to an ISO format string.
        ISO_format = '%Y-%m-%dT%H:%M:%S.%f'
        dt_str = bm1.updated_at.strftime(ISO_format)
        self.assertEqual(dt_str, bm1.updated_at.isoformat())

        # Storage is referred to as to update a JSON file, use save().
        bm1.save()
        self.assertTrue(os.path.isfile(storage._FileStorage__file_path))
        with open(storage._FileStorage__file_path, encoding='utf-8') as file:
            self.assertIn('BaseModel.' + bm1.id, json.load(file))

    def test_to_dict(self):
        """The public instance method `to_dict` is put to the test.
        """
        # Usage of normal:
        bm1 = BaseModel()

        # a dictionary is returned.
        self.assertIs(type(bm1.to_dict()), dict)

        # yields a dict containing all self members.__dict__
        for item in bm1.__dict__:
            self.assertIn(item, bm1.to_dict())

        # Returned dict also includes self.as '__class__' __class__.__name__
        bm1_dict = bm1.to_dict()
        self.assertIn('__class__', bm1_dict)
        self.assertEqual(bm1.__class__.__name__, bm1_dict['__class__'])

        # Returned dict includes self.created_at is same as 'created_at'.
        self.assertIn('created_at', bm1_dict)
        self.assertEqual(bm1.created_at.isoformat(),
                         bm1_dict['created_at'])

        # Returned dict also includes self.renamed updated_at to 'updated_at'
        self.assertIn('updated_at', bm1_dict)
        self.assertEqual(bm1.updated_at.isoformat(),
                         bm1_dict['updated_at'])
