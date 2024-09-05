#!/usr/bin/env python3
"""Initializes the storage system"""

from models.engine.db_storage import DBStorage

# Initialize storage
storage = DBStorage()

# Call reload method to load data (if needed)
storage.reload()

