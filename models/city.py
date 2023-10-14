#!/usr/bin/python3
"""Class `BaseModel` is part of AirBnB clone project."""
from .base_model import BaseModel


class City(BaseModel):
    """Defines `City` qualities.

    Attributes:
        state_id (str)
        name (str)
    """

    state_id = ""
    name = ""
