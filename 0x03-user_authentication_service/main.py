#!/usr/bin/env python3
"""
Main file
"""
from user import User
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from auth import _hash_password

print(User.__tablename__)
my_db = DB()

for column in User.__table__.columns:
    print("{}: {}".format(column, column.type))

user_1 = my_db.add("test@test.com", "SuperHashedPwd")
print(user_1.id)

user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
print(user_2.id)

find_user = my_db.find_user_by(email="test2@test.com")
print(find_user.id)

try:
    find_user = my_db.find_user_by(email="test2@test.com")
    print(find_user.id)
except NoResultFound:
    print("Not Found")

try:
    find_user = my_db.find_user_by("test@test.com")
    print(find_user.id)
except InvalidRequestError:
    print("Invalid")

print(_hash_password("Hello Holberton"))