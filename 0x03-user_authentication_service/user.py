#!/usr/bin/env python3
"""Houses the implementation of an SQLAlchemy model, named User"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String
)
from sqlalchemy.orm import DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


class User(Base):
    """User model which maps its attributes as a table fields or columns

    The model will have the following attributes:

    id, the integer primary key
    email, a non-nullable string
    hashed_password, a non-nullable string
    session_id, a nullable string
    reset_token, a nullable string
    """
    __tablename__ = 'users'
    id: Column = Column(Integer, primary_key=True)
    email: Column = Column(String(250), nullable=False)
    hashed_password: Column = Column(String(250), nullable=False)
    session_id: Column = Column(String(250), nullable=True)
    reset_token: Column = Column(String(250), nullable=True)
