import FreeCC_psg as FreeCC
import knownQueries_psg as sql_strings
import db_session

def get_db(query=sql_strings.show):

  temp_connection = None
  conn = db_session.active_connection

  if conn is None:
    temp_connection = db_session.open_connection('postgres', server_level=True)
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

  connection = db_session.open_connection('postgres', server_level=True)
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

  active_db = db_session._get_active_db_name(db_session.active_connection)
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

  typed_name = input(
      "Type the full name of the data base you want to delete: "
  ).strip()
  if typed_name != db_name:
    print(sql_strings.cancel_action)
    return

  sql_cmd = sql_strings.delete_db.replace("dummy_db", db_name)
  connection = db_session.open_connection("postgres", server_level=True)
  if connection is None:
    return

  try:
    FreeCC.execute_query(connection, sql_cmd)
    print("[Out]:", sql_cmd)
  finally:
    connection.close()
