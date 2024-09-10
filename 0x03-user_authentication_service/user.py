#!/usr/bin/env python3
"""Houses the implementation of an SQLAlchemy model, named User"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String
)

Base = declarative_base()


class User(Base):
    """User model which maps its attributes as a table fields or columns
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
