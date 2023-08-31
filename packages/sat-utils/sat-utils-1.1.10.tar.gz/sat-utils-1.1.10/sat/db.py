from enum import Enum

import cx_Oracle
import pyodbc


class SatDBException(BaseException):
    def __init__(self, message, error):
        super().__init__(message)
        self.error = error


class ConnectionType(Enum):
    ORACLE = 1
    SQL = 2


def get_db_connection(conn_string: str, conn_type: ConnectionType):
    """
    A function that returns a database connection.

    Parameters
    ----------
    conn_string: str
        The database specific connection string you are opening
         a connection to.
    conn_type: ConnectionType
        The database driver the connection uses.
    Returns
    -------
    A database connection object.
    """
    try:
        if conn_type == ConnectionType.SQL:
            return pyodbc.connect(conn_string)
        return cx_Oracle.connect(conn_string)
    except Exception as error:
        raise SatDBException(
            f"There was an {error.__class__.__name__} when connecting to the database.", error
        )
