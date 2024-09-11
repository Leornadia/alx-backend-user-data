#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User  # Import Base and User models


class DB:
    """DB class to handle database interactions.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        # Create a new SQLite engine instance with echo set to False
        self._engine = create_engine("sqlite:///a.db", echo=False)
        
        # Drop all tables in case they already exist (start fresh)
        Base.metadata.drop_all(self._engine)
        
        # Create all tables defined in Base (in this case, the User table)
        Base.metadata.create_all(self._engine)
        
        # Initialize the session to None
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Adds a new user to the database.
        
        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created User object.
        """
        # Create a new User instance
        new_user = User(email=email, hashed_password=hashed_password)
        
        # Add the user to the session
        self._session.add(new_user)
        
        # Commit the session to save the user to the database
        self._session.commit()
        
        # Refresh the session to update the new user object with the database-generated ID
        self._session.refresh(new_user)
        
        return new_user

