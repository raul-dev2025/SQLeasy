import os
import FreeCC_psg as FreeCC
import knownQueries_psg as sql_strings

active_connection = None


def get_dbName(dbName=sql_strings.defaultdB):
  """
  A function to set up the database name.
  Defaults to config file set up. Use this argument to config
  a new value in run time.
  """
  return dbName

def get_vault_config():
  """
  A function to read configuration variables from the vault path/file
  defined in knownQueries_psg. Parses KEY=VALUE lines into a dictionary.
  """
  base_path = os.path.dirname(os.path.abspath(__file__))
  target_file = getattr(sql_strings, "vault", ".hatch")
  file_path = os.path.join(base_path, target_file)

  config = {}
  with open(file_path, mode="r", encoding="utf-8") as a_file:
    for line in a_file:
      if "=" in line and not line.strip().startswith("#"):
        key, value = line.strip().split("=", 1)
        config[key.strip()] = value.strip()

  return config

def open_connection(db_name, server_level=False):
  """
  Open a connection to the target database using vault credentials.
  """
  config = get_vault_config()
  connector = (
      FreeCC.create_server_connection
      if server_level
      else FreeCC.create_db_connection
  )
  return connector(
      config.get("DB_HOST"),
      config.get("DB_USER"),
      config.get("DB_PASS"),
      db_name,
  )

def test_connection():
  """
  Test The SQL server state. Expected result: successful connection.
  Be sure the server is up an running before to try a connection.
  """
  config = get_vault_config()
  connection = FreeCC.create_server_connection(
      config.get("DB_HOST"),
      config.get("DB_USER"),
      config.get("DB_PASS"),
      get_dbName("postgres"),
  )

  if connection is None:
    return False

  connection.close()
  return True

def connect_to_database():
  """
  Lists available databases, resolves user selection by index, and connects via open_connection.
  """
  global active_connection
  from SQLeasy_psg import list_dataBases, select_db_by_index

  db_list = list_dataBases()
  if not db_list:
    return None

  selected_db = select_db_by_index(db_list)
  if not selected_db:
    return None

  new_conn = open_connection(selected_db)
  if new_conn is None:
    return None

  if active_connection is not None and active_connection is not new_conn:
    active_connection.close()

  active_connection = new_conn
  return active_connection

def run_with_connection(query_func, *args, **kwargs):
  """
  Auxiliar function to conntect secureley a DB and interrupt it, if
  the user aborts operation with 'q'.
  """
  global active_connection
  if active_connection is None:
    print(sql_strings.connection_failed)
    return

  if args:
    from SQLeasy_psg import clear_screen
    clear_screen()
    print("\n[Out]:", args[0])

  query_func(active_connection, *args, **kwargs)

def _get_active_db_name(conn):
  """
  Safely extracts the connected database name from active_connection if available.
  """
  if conn is None:
    return None

  info = getattr(conn, "info", None)
  if info is not None:
    db_name = getattr(info, "dbname", None)
    if db_name:
      return db_name

  dsn = getattr(conn, "dsn", None)
  if isinstance(dsn, str) and "dbname=" in dsn:
    for part in dsn.split():
      if part.startswith("dbname="):
        return part.split("=", 1)[1]

  return None

def get_active_db_label(connection, default_db=sql_strings.defaultdB):
  """
  Resolve the active database label for menu display.
  """
  if connection is None:
    return "NONE (Select a database first)"

  info = getattr(connection, "info", None)
  db_name = getattr(info, "dbname", None)

  if not db_name or db_name == default_db:
    return "NONE (Select a database first)"

  return db_name