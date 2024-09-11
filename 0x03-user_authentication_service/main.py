#!/usr/bin/env python3
"""
Main file
"""
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

# Define the SQLAlchemy Base and User model
Base = declarative_base()

class User(Base):
    """User model mapped to the 'users' table in the database."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

# Define the DB class to handle database operations
class DB:
    """DB class to handle database interactions."""

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
            # Use the filter_by method to filter by the given keyword arguments
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No result found for the given query.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid arguments provided for query.")

    def update_user(self, user_id: int, **kwargs: str) -> None:
        """Updates a user's attributes in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Keyword arguments representing the attributes to update.

        Raises:
            ValueError: If an argument does not correspond to a user attribute.
        """
        user = self._session.query(User).filter_by(id=user_id).first()
        if user is None:
            raise ValueError(f"User with ID {user_id} not found.")

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)

        self._session.commit()

# Main testing part
if __name__ == "__main__":
    # Print table schema
    print(User.__tablename__)

    for column in User.__table__.columns:
        print("{}: {}".format(column, column.type))

    # Create an instance of the DB class
    my_db = DB()

    # Add a new user to the database
    user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
    print(user_1.id)

    # Add another user to the database
    user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
    print(user_2.id)

    # Find user by email
    find_user = my_db.find_user_by(email="test@test.com")
    print(find_user.id)

    # Test finding a non-existent user
    try:
        find_user = my_db.find_user_by(email="test2@test.com")
        print(find_user.id)
    except NoResultFound:
        print("User not found")

    # Test finding with an invalid query argument
    try:
        find_user = my_db.find_user_by(no_email="test@test.com")
        print(find_user.id)
    except InvalidRequestError:
        print("Invalid request")

    # Update the user's password
    try:
        my_db.update_user(user_1.id, hashed_password='NewPwd')
        print("Password updated")

        # Print the updated user's attributes
        updated_user = my_db.find_user_by(id=user_1.id)
        print(f"Updated User: id={updated_user.id}, email={updated_user.email}, hashed_password={updated_user.hashed_password}, session_id={updated_user.session_id}, reset_token={updated_user.reset_token}")

    except ValueError:
        print("Error")
