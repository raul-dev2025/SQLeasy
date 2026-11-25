import pandas as pd
import FreeCC_psg as FreeCC, display_initiator_psg as display_initiator
import knownQueries_psg as sql_strings
import db_session

def createTable(default=sql_strings.create_table):
  """
  This method creates a table. As usual wrap the query fn() inside
  a python function-documentation block.

  :param default: not implemented yet.
  """
  db_session.run_with_connection(FreeCC.execute_query, default)

def deleteTable(default=sql_strings.delete_table):
  """
  This method deletes a table. As usual wrap the query fn() inside
  a python function-documentation block.

  :param default: not implemented yet.
  """
  db_session.run_with_connection(FreeCC.execute_query, default)

def start_query(default=sql_strings.show):
  """
  Starts a new query on the server side.

  :param default: default query. Positional, implicit named, called
    by omision.
  """
  if db_session.active_connection is None:
    print(sql_strings.connection_failed)
    return
  
  results = FreeCC.read_query(db_session.active_connection, default)
  for result in results:
    print(result)

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
  db_session.run_with_connection(FreeCC.execute_query, sql_strings.insert_multiple)

def delete_from_table():
  """
  Deletes records from a table. As usual wrap the query fn()
  inside a python function-documentation block.

  :param default: not implemented yet.
  """
  db_session.run_with_connection(FreeCC.execute_query, sql_strings.delete_entry)

def modify_table():
    """
    A function wrapper. It calls execute_query() wich takes two arguments.
    In fact, you can use this method to execute any query. As usual wrap the
    query fn() inside a python function-documentation block.

    :param default: not implemented yet.
    """
    db_session.run_with_connection(FreeCC.execute_query, sql_strings.orders_alter)

def modify_many_table():
    """
    A function wrapper. It calls execute_list_query().
    The function takes an extra argument; ``val``. It is a Python's object
    structure, a list of tuples. As usual wrap the query fn() inside a python
    function-documentation block and left the object untouched.

    :param default: not implemented yet.
    """
    db_session.run_with_connection(FreeCC.execute_list_query,
            sql_strings.insert_multiple,
            sql_strings.val)

def dump_html(default=sql_strings.q1):
  '''
  Specific to the Pandas library. Default's Pandas method requires a list of
  lists, as starting point to build the data frame(our database query). So
  we need to transform a list of tuples(the actual output), to a more
  convenient way, to work with the returned datum. It takes no arguments.
  This implementation is a "all-or-nothing" method, that writes the table
  directly into a "dump.html" file.
  '''
  if db_session.active_connection is None:
    print(sql_strings.connection_failed)
    return

  results = FreeCC.read_query(db_session.active_connection, default)
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
