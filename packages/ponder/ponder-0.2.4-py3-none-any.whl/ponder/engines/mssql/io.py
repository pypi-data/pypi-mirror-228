from __future__ import annotations

import logging

from modin.core.io.io import BaseIO

from ponder.core.query_tree import QueryTree
from ponder.engines.mssql.connection import MSSQLConnection

client_logger = logging.getLogger("client logger")


class MSSQLIO(BaseIO):
    dbms_connection = None

    @classmethod
    def from_pandas(cls, pdf, connection):
        if cls.dbms_connection is None:
            cls.dbms_connection = MSSQLConnection(connection)
        elif connection is not cls.dbms_connection.get_user_connection():
            client_logger.info("Resetting mssql connection to new connection")
            cls.dbms_connection = MSSQLConnection(connection)
        return QueryTree.make_tree_from_pdf(cls.dbms_connection, pdf)
