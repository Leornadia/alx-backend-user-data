#!/usr/bin/env python3
"""
Database module for user authentication service.
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()


class User(Base):
    """
    User class to represent a user in the database.
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)


class DB:
    """
    DB class to handle database operations.
    """

    def __init__(self):
        """
        Initialize a new DB instance.
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self._session = sessionmaker(bind=self._engine)()

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the query.

        Returns:
            User: The first User object found that matches the criteria.

        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If invalid query arguments are passed.
        """
        try:
            # Attempt to find the user by the provided keyword arguments
            user = self._session.query(User).filter_by(**kwargs).one_or_none()

            if user is None:
                # If no user is found, raise NoResultFound
                raise NoResultFound

            return user

        except InvalidRequestError as e:
            # Raise InvalidRequestError for invalid query arguments
            raise InvalidRequestError from e

        except NoResultFound as e:
            # Re-raise NoResultFound if no user is found
            raise NoResultFound from e

        except Exception as e:
            # Raise InvalidRequestError for any other unexpected exceptions
            raise InvalidRequestError from e

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user by user ID.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments to update in the user.

        Raises:
            ValueError: If user is not found.
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            raise ValueError(f"No user found with id {user_id}")

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        self._session.commit()

