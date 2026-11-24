import os
import pandas as pd
import FreeCC_psg as FreeCC, display_initiator_psg as display_initiator
import knownQueries_psg as sql_strings
import Queries.query_alter_tables_psg as qvar

active_connection = None

# get_machine()
# get_user()

def prompt_user():
  """
  Just another of those informational and tedious user prompts. Future
  implemetations of this function, could change their actual functionallity.

  :param return: name; user data.
  """
  name = input('>>> ')
  if not isinstance(name, str):
     print('Invalid entry...')

  return name

def clear_screen():
  """
  Clear the screen before executing the selected option.
  """
  os.system('cls' if os.name == 'nt' else 'clear')

def get_dbName(dbName=sql_strings.defaultdB):
  '''
  A function to set up the database name.
  Defaults to config file set up. Use this argument to config
  a new value in run time.

  :param dbName: var. Placeholder.
  :param return: return database name.
  :return: return database name.
  '''
  return dbName

def get_vault_config():
  '''
  A function to read configuration variables from the vault path/file 
  defined in knownQueries_psg. Parses KEY=VALUE lines into a dictionary.
  '''
  base_path = os.path.dirname(os.path.abspath(__file__))
  
  # Usamos un archivo por defecto o el nombre especificado en las variables
  target_file = getattr(sql_strings, 'vault', '.hatch')
  file_path = os.path.join(base_path, target_file)

  config = {}
  
  with open(file_path, mode='r', encoding='utf-8') as a_file:
    for line in a_file:
      if '=' in line and not line.strip().startswith('#'):
        key, value = line.strip().split('=', 1)
        config[key.strip()] = value.strip()
        
  return config

def open_connection(db_name, server_level=False):
  """
  Open a conncection to the target database using vault credentials.
  """
  config = get_vault_config()
  connector = (
    FreeCC.create_server_connection
    if server_level
    else FreeCC.create_db_connection
  )
  return connector(
    config.get('DB_HOST'),
    config.get('DB_USER'),
    config.get('DB_PASS'),
    db_name,
  )

def test_connection():
  '''
  Test The SQL server state. Expected result: successful connection.
  Be sure the server is up an running before to try a connection.

  :param return: return connection.
  '''

  config = get_vault_config()
  connection = FreeCC.create_server_connection(
    config.get('DB_HOST'),
    config.get('DB_USER'),
    config.get('DB_PASS'),
    get_dbName('postgres'),
  )

  if connection is None:
    return False

  connection.close()
  return True

def select_db_by_index(db_list):
  """
  Prompts for a 1-based database index from db_list and returns the database name.
  Prints sql_strings.cancel_action and returns None on empty/invalid/out-of-range input.
  """
  if not db_list:
    return None

  raw_choice = input(f"Select DataBase (1-{len(db_list)}): ").strip()
  if not raw_choice:
    print(sql_strings.cancel_action)
    return None
  
  try:
    choice = int(raw_choice)
  except ValueError:
    print(sql_strings.cancel_action)
    return None

  if choice < 1 or choice > len(db_list):
    print(sql_strings.wrongDb)
    return None

  return db_list[choice - 1]

def connect_to_database():
  """
  Lists available databases, resolves user selection by index, and connects via open_connection.
  """
  global active_connection

  db_list = list_dataBases()
  if not db_list:
    return

  selected_db = select_db_by_index(db_list)
  if not selected_db:
    return

  new_conn = open_connection(selected_db)
  if new_conn is None:
    return

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
    clear_screen()
    print("\n[Out]:", args[0])

  query_func(active_connection, *args, **kwargs)

def start_query(default=sql_strings.show):
  """
  Starts a new query on the server side.

  :param default: default query. Positional, implicit named, called
    by omision.
  """
  global active_connection
  if active_connection is None:
    print(sql_strings.connection_failed)
    return
  
  results = FreeCC.read_query(active_connection, default)
  for result in results:
    print(result)

def get_db(query=sql_strings.show):
  global active_connection

  temp_connection = None
  conn = active_connection

  if conn is None:
    temp_connection = open_connection('postgres', server_level=True)
    if temp_connection is None:
      return []
    conn = temp_connection

  try:
    rows = FreeCC.read_query(conn, query)
  finally:
    if temp_connection is not None:
      temp_connection.close()

  if not rows:
    return []

  return [row[0] for row in rows]

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

def list_dataBases():
  """
  Loops in a database list.
  """
  db_list = get_db()
  if not db_list:
    print("No databases available")
    return []
  
  col_width = 25
  row = []

  for idx, db_name in enumerate(db_list, start=1):
    label = f"  {idx}. {db_name}"
    if len(label) > col_width:
      label = f"{label[: col_width -2]}.."
    cell = label.ljust(col_width)
    row.append(cell)

    if len(row) == 3:
      print("".join(row))
      row = []

  if row:
    print("".join(row))

  return db_list

def create_DB(db_name=None):
  """
  A method creates a database. As usual wrap the query fn() inside
  a python function-documentation block.
  """
  sql_cmd = sql_strings.create_db

  if db_name is None:
    print(sql_strings.chosedB.format(sql_cmd))
    print(f"sql template: {sql_cmd}")
    user_input = input('>>> ').strip()
    if not user_input or user_input.lower() == 'q':
      print("\nCanceled action.")
      return
    db_name = user_input

  sql_cmd = sql_cmd.replace('dummy_db', db_name)
  print(f"Prepared SQL: {sql_cmd}")

  connection = open_connection('postgres', server_level=True)
  if connection is None:
    return

  try:
    FreeCC.create_database(connection, sql_cmd)
    print('[Out]: ', sql_cmd)
  finally:
    connection.close()

def delete_DB(db_name=None):
  """
    Deletes a database after index selection, protected/active DB checks,
    and two-step confirmation (y/yes + exact database name). 283 - 322
  """
  PROTECTED_DBS = {"postgres"}

  if db_name is None:
    db_list = list_dataBases()
    if not db_list:
      return
  
    db_name = select_db_by_index(db_list)
    if not db_name:
      return

  if db_name in PROTECTED_DBS:
    print(f"Cannot delete protected database '{db_name}'.")
    print(sql_strings.cancel_action)
    return

  active_db = _get_active_db_name(active_connection)
  if active_db == db_name:
    print(
        f"Database '{db_name}' is currently active. Switch to another"
        " database before deleting it."
    )
    print(sql_strings.cancel_action)
    return

  print(sql_strings.atention)
  confirm_choice = (
      input(f"Do you want to delete db {db_name}? [y|yes] / [n|no]: ")
      .strip()
      .lower()
  )
  if confirm_choice not in ("y", "yes"):
    print(sql_strings.cancel_action)
    return

  sql_cmd = sql_strings.delete_db.replace('dummy_db', db_name)
  connection = open_connection('postgres', server_level=True)
  if connection is None:
    return

  try:
    FreeCC.execute_query(connection, sql_cmd)
    print('[Out]:', sql_cmd)
  finally:
    connection.close()

def createTable(default=sql_strings.client_table):
  """
  This method creates a table. As usual wrap the query fn() inside
  a python function-documentation block.

  :param default: not implemented yet.
  """
  run_with_connection(FreeCC.execute_query, default)

def deleteTable():
  """
  This method deletes a table. As usual wrap the query fn() inside
  a python function-documentation block.

  :param default: not implemented yet.
  """
  run_with_connection(FreeCC.execute_query, sql_strings.delete_table)

def insert_into_table():
  """
  Insert into table <table name>. It takes no arguments;
  just remember to not overlap the index on automatic fields
  where the table definition field is configured as an
  'AUTO_INCREMENT' value.
  Push the row value for the 'AUTO_INCREMENT' field as NULL;
  otherwise the table will end up with an index field -usually,
  overlapping identifiers.

  The query saved as python string, is the main entry point.
  Use that to adjust the task.
  """
  run_with_connection(FreeCC.execute_query, sql_strings.insert_multiple)

def delete_from_table():
  """
  Deletes records from a table. As usual wrap the query fn()
  inside a python function-documentation block.

  :param default: not implemented yet.
  """
  run_with_connection(FreeCC.execute_query, sql_strings.delete_entry)

def modify_table():
    """
    A function wrapper. It calls execute_query() wich takes two arguments.
    In fact, you can use this method to execute any query. As usual wrap the
    query fn() inside a python function-documentation block.

    :param default: not implemented yet.
    """
    run_with_connection(FreeCC.execute_query, qvar.orders_alters)
    # placeHere_extra_calls(one per table). Just remember the correct selector.
    # ie:
    # import statement, connection definition(1), fn_call(many)

    # separator

def modify_many_table():
    """
    A function wrapper. It calls execute_list_query().
    The function takes an extra argument; ``val``. It is a Python's object
    structure, a list of tuples. As usual wrap the query fn() inside a python
    function-documentation block and left the object untouched.

    :param default: not implemented yet.
    """
    run_with_connection(FreeCC.execute_list_query, sql_strings.insert_multiple, sql_strings.val)

def dump_html(default=sql_strings.q1):
  '''
  Specific to the Pandas library. Default's Pandas method requires a list of
  lists, as starting point to build the data frame(our database query). So
  we need to transform a list of tuples(the actual output), to a more
  convenient way, to work with the returned datum. It takes no arguments.
  This implementation is a "all-or-nothing" method, that writes the table
  directly into a "dump.html" file.
  '''
  global active_connection
  if active_connection is None:
    print(sql_strings.connection_failed)
    return

  results = FreeCC.read_query(active_connection, default)
  a_list = []
  for result in results:
    result = list(result)
    a_list.append(result)

  columns = sql_strings.p_columnus
  df = pd.DataFrame(a_list, columns=columns)
  print(df)

  with open('dump.html', mode="w", encoding="utf-8") as a_file:
    html = df.to_html(index=False)
    a_file.write(html)

  display_initiator.dump_html_styled('dump.html')

def get_active_db_label(connection, default_db=sql_strings.defaultdB):
  """
  Resolve the active database label for menu display.

  :param connection: active PostgreSQL connection object or None.
  :param default_db: default placeholder value from configuration.
  :return: formatted database label string.
  """
  if connection is None:
    return "NONE (Select a database first)"

  info = getattr(connection, "info", None)
  db_name = getattr(info, "dbname", None)

  if not db_name or db_name == default_db:
    return "NONE (Select a database first)"

  return db_name

# punto de entrada a la aplicacion
def init_app():
  """
  1. Print the formatted message in columns.
  2. Retrieve the options dictionary mapping numbers to functions.
  3. Capture the user input option within a persistent loop.
  """
  global active_connection
  clear_screen()
  print(sql_strings.init_app)
  active_connection = connect_to_database()

  if active_connection is None:
    print(sql_strings.fail_con)
    return

  clear_screen()

  while True:
    active_db_label = get_active_db_label(active_connection)
    print(sql_strings.message.format(active_db=active_db_label))
    options = display_initiator.display_options()
    fn = input('>>> ')

    # Manejar la salida si el usuario pulsa 'q'
    if fn.lower() == 'q':
        print("Saliendo de SQLeasy...")
        if active_connection:
          active_connection.close()
        break

    # Ejecutar la opción seleccionada si existe en el diccionario
    if fn in options:
        clear_screen()
        exec(options[fn])
        input("\nPresiona Enter para continuar...")
        clear_screen()
    else:
        print("Error: Opción no válida.")



if __name__ == "__main__":
  init_app()

# pdb.run('init_app()')
