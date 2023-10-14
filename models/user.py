#!/usr/bin/python3
""" class `class User` is of AirBnB clone project. """
from .base_model import BaseModel


class User(BaseModel):
    """Defines the `User` characteristics.

    Attributes:
        email (str)
        password (str)
        first_name (str)
        last_name (str)

    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
