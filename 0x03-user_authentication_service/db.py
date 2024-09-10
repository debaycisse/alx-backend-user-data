#!/usr/bin/env python3
"""This module houses the implementation of the DB class"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User
from typing import (
    Union,
    List,
    Dict,
    Any
)
import bcrypt


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session: Union[Session, None] = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a user object to the database"""
        user = User(email=email, hashed_password=hashed_password)
        session: Session = self._session
        try:
            session.add(user)
            session.commit()
        except Exception as e:
            session.rollback()
        return user

    def find_user_by(self, *args: List, **kwargs: Any) -> User:
        """Finds a given user based a given keyword argument(s)

        Args:
            args - a list of arguments, passed to the method
            kwargs - a list of keyword arguments, passed to this method

        Returns:
            An instance of the user class, if found, otherwise
            NoResultFound and InvalidRequestError are raised
        """
        session: Session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
        except NoResultFound:
            raise NoResultFound
        except InvalidRequestError:
            raise InvalidRequestError
        return user

    def update_user(self, user_id: int, **kwargs: Any) -> None:
        """Updates a given user with a given attributes

        Args:
            user_id - the id of the user instance
            whose attributes are to be updated
            kwargs - a list of arbitrary keyword arguments
        """
        session: Session = self._session
        user = self.find_user_by(id=user_id)
        if not (user is None):
            try:
                for k, v in kwargs.items():
                    if hasattr(user, k):
                        setattr(user, k, v)
                    else:
                        raise ValueError
            except ValueError:
                session.rollback()
                raise ValueError("Invalid attribute")
            session.commit()
