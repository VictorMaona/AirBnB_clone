#!/usr/bin/python3
"""represents an Amenity in AirBnB clone project"""
from .base_model import BaseModel


class Amenity(BaseModel):
    """inherit specific traits methods `Amenity`.

    Attributes:
        name (str)
    """

    name = ""
