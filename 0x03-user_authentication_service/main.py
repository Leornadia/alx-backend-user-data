#!/usr/bin/env python3
"""
Main file to initialize the database and test the add_user method.
"""

from db import DB  # Import the DB class
from user import User  # Import the User model

def main():
    # Initialize the database
    my_db = DB()

    # Print table name and column information
    print(User.__tablename__)
    for column in User.__table__.columns:
        print("{}: {}".format(column, column.type))
    
    # Add users and print their IDs
    user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
    print(user_1.id)

    user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
    print(user_2.id)

if __name__ == "__main__":
    main()

