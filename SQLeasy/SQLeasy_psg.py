import os
import pandas as pd
import FreeCC_psg as FreeCC, display_initiator
import knownQueries_psg as sql_strings
import Queries.query_alter_tables as qvar



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

  # separator

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
    config.get('DB_NAME'),    
  )

  return connection

def connect_to_database(dbName=sql_strings.defaultdB):
  """
  Connect to available database.

  :param dbName: default value. Positional, implicit named, called
                 by omision.
  :param return: return connection.
  """
  print(sql_strings.selectDb)
  list_dataBases()
  userInput = input('>>> ')

  target_db = userInput if userInput else dbName

  if (target_db in sql_strings.dbNames):
    config = get_vault_config()
    connection = FreeCC.create_db_connection(
      config.get('DB_HOST'),
      config.get('DB_USER'),
      config.get('DB_PASS'),
      target_db
    )
    print('\t{} Connection established'.format(target_db))
  else:
    print(sql_strings.wrongDb, '', target_db)
    connection = None

  return connection

def start_query(default=sql_strings.default_query):
  """
  Starts a new query on the server side.

  :param default: default query. Positional, implicit named, called
    by omision.
  """
  config = get_vault_config()
  dbName = get_dbName()
  connection = FreeCC.create_db_connection(
    config.get('DB_HOST'),
    config.get('DB_USER'),
    config.get('DB_PASS'),
    dbName
  )  
  results = FreeCC.read_query(connection, sql_strings.default_query)
  for result in results:
    print(result)

def list_dataBases():
  """
  Loops in a database list.
  """
  # global dbNames
  for dbName in sql_strings.dbNames:
    print('\t', dbName)
    # print(dbNames.index(dbName), '-', dbName)

def replace_sql_cmd():
  # file = sql_strings.file
  sql_cmd = sql_strings.create_dummyDB
  print(sql_strings.chosedB.format(sql_cmd))
  list_dataBases()
  dbName = input('>>> ')
  if not isinstance(dbName, str):
     print('Invalid entry...')
  sql_cmd = sql_cmd.replace('dummy_db', dbName)

  connection = test_connection()
  FreeCC.create_database(connection, sql_cmd)
  # print('[Out]: ', sql_cmd)


  # return cursor

def create_db():
  """
  A method creates a database. As usual wrap the query fn() inside
  a python function-documentation block.
  """
  replace_sql_cmd()

  # separator

def delete_db():
  """
  Delete the Data Base name. Defuaults to configuration variable
  defined in respective file. Look in documentation pages to refer it.
  From your configutation file you can adapt the message to your special
  needs, including this note.

  A confirmation message pop-up, requiring your ATENTION. Possible answers
  expected <[y], [yes], [Y], [YES]>. No defaults yet implemented, white
  blanks, carriage return, or break commands should be ignored. Other
  values <[n], [no], [N], [NO]> will be considered as a negative answer
  in the same way.

  :param pram: description param.
  """
  print(sql_strings.atention)
  confirmation = input('>>> [y]/[n] >>>: '); print(confirmation)
  if (confirmation == 'y'):
    print(sql_strings.typeName)
    dbName = prompt_user()
    sql_cmd = sql_strings.delete_dummyDB
    sql_cmd = sql_cmd.replace('dummy_db', dbName)
    connection = test_connection()
    FreeCC.execute_query(connection, sql_cmd)
  else:
    print(sql_strings.cancel_action)

    # separator

def create_table():
  """
  This method creates a table. As usual wrap the query fn() inside
  a python function-documentation block.

  :param default: not implemented yet.
  """
  connection = connect_to_database()
  FreeCC.execute_query(connection, sql_strings.create_dummy_table)

  # separator

def delete_table():
  """
  This method deletes a table. As usual wrap the query fn() inside
  a python function-documentation block.

  :param default: not implemented yet.
  """
  connection = connect_to_database()
  FreeCC.execute_query(connection, sql_strings.delete_dummy_table)

  # separator

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
  connection = connect_to_database()
  FreeCC.execute_query(connection, sql_strings.pop_dummy)

  # separator

def delete_from_table():
  """
  Deletes records from a table. As usual wrap the query fn()
  inside a python function-documentation block.

  :param default: not implemented yet.
  """
  connection = connect_to_database()
  FreeCC.execute_query(connection, sql_strings.delete_entry)

  # separator

def modify_table():
    """
    A function wrapper. It calls execute_query() wich takes two arguments.
    In fact, you can use this method to execute any query. As usual wrap the
    query fn() inside a python function-documentation block.

    :param default: not implemented yet.
    """
    connection = connect_to_database()
    FreeCC.execute_query(connection, qvar.orders_alters)
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
    connection = connect_to_database()
    FreeCC.execute_list_query(connection, sql_strings.sql, sql_strings.val)

    # separator

def dump_html():
  '''
  Specific to the Pandas library. Default's Pandas method requires a list of
  lists, as starting point to build the data frame(our database query). So
  we need to transform a list of tuples(the actual output), to a more
  convenient way, to work with the returned datum. It takes no arguments.
  This implementation is a "all-or-nothing" method, that writes the table
  directly into a "dump.html" file.
  '''
  connection = connect_to_database()
  results = FreeCC.read_query(connection, sql_strings.q1)
  a_list = []
  for result in results:
    result = list(result)
    a_list.append(result)

  columns = sql_strings.p_columnus
  df = pd.DataFrame(a_list, columns=columns)
  display(df)

  with open('dump.html', mode="w", encoding="utf-8") as a_file:
    html = df.to_html()
    a_file.write(html)

def init_app():
  """Documentation"""
  options = display_initiator.display_options()
  fn = input('>>> ')
  fn = options[fn]
  exec(fn)




if __name__ == "__main__":
  init_app()

# pdb.run('init_app()')
