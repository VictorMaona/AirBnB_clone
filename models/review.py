#!/usr/bin/python3
"""class `class Review` is of AirBnB clone project."""
from .base_model import BaseModel


class Review(BaseModel):
    """Defines the `Review` characteristics.

    Attributes:
        place_id (str)
        user_id (str)
        text (str)
    """

    place_id = ""
    user_id = ""
    text = ""
