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

def _extract_max_length(err):
  """Extract the maximum allowed length N from a character varying(N) or varchar(N) error.

  Args:
      err: Exception instance or error message containing the length limit.

  Returns:
      int | None: The extracted length limit as an integer, or None if not found.
  """
  if err is None:
    return None

  match = re.search(r"\b(?:character varying|varchar)\s*\(\s*(\d+)\s*\)", str(err), re.IGNORECASE)
  if match:
    return int(match.group(1))

  return None

InterfaceError

DatabaseError / Error




