#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Method Add a new user to the database.

        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The User object that was added to the database.
        """
        # Create a new User object
        new_user = User(email=email, hashed_password=hashed_password)

        # Add the new user to the session
        self._session.add(new_user)

        try:
            # Commit the changes to the database
            self._session.commit()
        except IntegrityError as e:
            # Handle any integrity errors, such as duplicate email
            self._session.rollback()
            raise e

        # Return the newly created User object
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        This Method Finds and return the first user that matches
        the provided filter conditions.

        Args:
            **kwargs: Arbitrary keyword arguments
            representing filter conditions.

        Returns:
            User: The User object that matches the
            filter conditions.

        Raises:
            NoResultFound: If no results are found based
            on the filter conditions.
            InvalidRequestError: If invalid query arguments
            are passed.
        """
        try:
            # Query the database to find the first user that
            # matches the filter conditions
            user = self._session.query(User).filter_by(**kwargs).first()

            if user is None:
                raise NoResultFound(
                    "No user found matching the filter conditions"
                )

            return user
        except InvalidRequestError as e:
            self._session.rollback()
            raise e
