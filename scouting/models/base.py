from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy.ext.declarative import declarative_base

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class ValidationError(Exception):
    """An exception for when data from a form doesn't validate.

    This exception is for use in the validate methods of the models when the
    data given to them doesn't validate.

    Attributes:
        message:  A message describing why the data doesn't validate
        values: A dictionary of the values which where given to the model to
            validate.
    """
    def __init__(self, message, values):
        """Initialises the exception,

        Args:
            message:  A message describing why the data doesn't validate
            values: A dictionary of the values of the model replaced with the
                values which were in the submitted form.
        """
        self.message = message
        self.values = values
