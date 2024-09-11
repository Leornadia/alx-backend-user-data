#!/usr/bin/env python3
"""
Main file
"""
from user import User
from db import DB
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

# Create a new DB instance and add two users to the database
my_db = DB()
user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")

# Find a user by email and print their ID
find_user = my_db.find_user_by(email="test@test.com")

# Try to find a user by email that doesn't exist and handle the NoResultFound exception
try:
    find_user = my_db.find_user_by(email="test2@test.com")
except NoResultFound:
    pass

# Try to find a user by an invalid attribute and handle the InvalidRequestError exception
try:
    find_user = my_db.find_user_by(no_email="test@test.com")
except InvalidRequestError:
    pass

# Update a user's hashed password and handle the ValueError exception
email = 'test@test.com'
hashed_password = "hashedPwd"
user = my_db.add_user(email, hashed_password)
try:
    my_db.update_user(user.id, hashed_password='NewPwd')
except ValueError:
    pass

if __name__ == "__main__":
    # Print the name of the User table and the type of each column in the table
    print(User.__tablename__)
    for column in User.__table__.columns:
        print("{}: {}".format(column, column.type))

