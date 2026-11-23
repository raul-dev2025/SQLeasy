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

def _find_length_overflow(sql, val, max_length):
  """Locate columns and rows whose string values exceed max_length in an INSERT statement.

  Args:
      sql: SQL INSERT statement string with explicit target columns.
      val: A single row sequence or a sequence of row sequences passed as query parameters.
      max_length: Maximum allowed character length for string values.
  
  Returns:
      list[dict]: Dictionaries describing each overflow with keys 'column',
          'row', 'length', and 'max_length'.
   """
  overflow = []

  if not sql or val is None or max_length is None:
    return overflow

  match = re.search(r"\bINSERT\s+INTO\s+\S+\s*\(([^)]+)\)", sql, re.IGNORECASE)
  if not match:
    return overflow

  columns = [col.strip().strip('"') for col in match.group(1).split(",")]

  if isinstance(val, (list, tuple)) and val and isinstance(val[0], (list, tuple)):
    rows = val
  elif isinstance(val,(list, tuple)):
    rows = [val]
  else:
    return overflow

  for row_idx, row in enumerate(rows, start=1):
    for col_name, value in zip(columns, row):
      if isinstance(value, str) and len(value) > max_length:
        overflow.append({
          "column": col_name,
          "row": row_idx,
          "length": len(value),
          "max_length": max_length,
        })

  return overflow





