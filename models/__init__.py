#!/usr/bin/python3
"""initializes the storage mechanism"""
from .engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
