from unittest.mock import patch

import pytest
from cx_Oracle import DatabaseError
from pyodbc import InterfaceError
from sat.db import ConnectionType as ctype
from sat.db import SatDBException, get_db_connection


def test_pyodbc_errors():
    with patch("sat.db.pyodbc") as mock_pyodbc:
        conn_string = "Bad Connection String"
        mock_pyodbc.connect.side_effect = InterfaceError("Thrown interface error.")
        with pytest.raises(SatDBException) as ex:
            get_db_connection(conn_string, ctype.SQL)
    assert "InterfaceError" in str(ex.value)
    assert "Thrown interface error." in str(ex.value.error)


def test_oracle_error():
    with patch("sat.db.cx_Oracle") as mock_oracle:
        conn_string = "Test Connection String"
        mock_oracle.connect.side_effect = DatabaseError("Thrown database error.")
        with pytest.raises(SatDBException) as ex:
            get_db_connection(conn_string, ctype.ORACLE)
    assert "DatabaseError" in str(ex.value)
    assert "Thrown database error." in str(ex.value.error)
