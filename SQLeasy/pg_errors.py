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

def _format_data_error(err, sql=None, val=None):
  """Format a psycopg2 DataError into a clear, actionable diagnostic message.

  Args:
      err: The DataError exception raised by psycopg2.
      sql: Optional SQL statement associated with the failed execution.
      val: Optional bound parameters associated with the failed execution.

  Returns:
      str: Formatted diagnostic message including overflow details when available.
  """
  max_length = _extract_max_length(err)
  overflow = _find_length_overflow(sql, val, max_length)

  if overflow:
    details = [
      f"column '{item['column']}' (row {item['row']}): length {item['length']} > max {item['max_length']}"
      for item in overflow
    ]
    return f"DataError (length overflow): {'; '.join(details)} | Original error: {str(err).strip()}"

  if max_length is not None:
    return f"DataError (max length {max_length}): {str(err).strip()}"
  
  return f"DataError: {str(err).strip()}"
            
def handle_pg_error(err, connection=None, sql=None, val=None, rollback=True):
  """Handle psycopg2 exceptions centrally and return a clear diagnostic message.

  Classifies psycopg2 exceptions from most specific to most general:
  - psycopg2.DataError: Delegates to _format_data_error() for length overflow diagnostics.
  - psycopg2.IntegrityError: Reports constraint violations (unique, foreign key, NOT NULL, etc.).
  - psycopg2.ProgrammingError: Reports SQL syntax, missing object, or parameter mismatches.
  - psycopg2.OperationalError: Reports connection, network, or server-level issues.
  - psycopg2.InterfaceError: Reports misuse of the connection or cursor interface.
  - psycopg2.DatabaseError / psycopg2.Error: Reports general database or PostgreSQL errors.

  Args:
      err: The raised exception instance.
      connection: Optional psycopg2 connection used for transaction rollback.
      sql: Optional SQL statement for diagnostic context.
      val: Optional parameter values for diagnostic context.
      rollback: Whether to roll back the transaction safely before formatting the error.

  Returns:
      str: Clear diagnostic summary for logging or error reporting.
    """
  if rollback:
    _safe_rollback(connection)

  detail = str(err).strip() if err is not None else ""

  if isinstance(err, psycopg2.DataError):
    return _format_data_error(err, sql=sql, val=val)
  if isinstance(err, psycopg2.IntegrityError):
    return f"IntegrityError (constraint overflow): {detail}"
  if isinstance(err, psycopg2.ProgrammingError):
    return f"ProgrammingError (SQL or schema issue): {detail}"
  if isinstance(err, psycopg2.OperationalError):
    return f"OperationalError (connection or server issue): {detail}"
  if isinstance(err, psycopg2.InterfaceError):
    return f"InterfaceError (connection or cursor usage): {detail}"
  if isinstance(err, psycopg2.DatabaseError):
    return f"DatabaseError: {detail}"
  if isinstance(err, psycopg2.Error):
    return f"PostgreSQL Error: {detail}"

  return f"Unexpected Error ({type(err).__name__}): {detail}"