import re, psycopg2


def _safe_rollback(connection):
  """Safely roll back an aborted or failed transaction on the active connection.

    Args:
        connection: A psycopg2 connection object, None, or an already closed
            connection without an active transaction.
    """
  if connection is not None:
    try:
      connection.rollback()
    except Exception:
      pass

_safe_rollback

DataError

IntegrityError

ProgrammingError

OperationalError

InterfaceError

DatabaseError / Error




