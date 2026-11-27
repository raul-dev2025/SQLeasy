import os
import display_initiator_psg as display_initiator
import knownQueries_psg as sql_strings
import db_session, db_admin, data_ops, data_filters

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

def init_app():
  """
  1. Print the formatted message in columns.
  2. Retrieve the options dictionary mapping numbers to functions.
  3. Capture the user input option within a persistent loop.
  """  
  clear_screen()
  print(sql_strings.init_app)
  db_session.active_connection = db_session.connect_to_database()

  if db_session.active_connection is None:
    print(sql_strings.fail_con)
    return

  clear_screen()

  while True:
    active_db_label = db_session.get_active_db_label(db_session.active_connection)
    print(sql_strings.message.format(active_db=active_db_label))
    options = display_initiator.display_options()
    fn = input('>>> ')

    # Manejar la salida si el usuario pulsa 'q'
    if fn.lower() == 'q':
        print("Saliendo de SQLeasy...")
        if db_session.active_connection:
          db_session.active_connection.close()
          db_session.active_connection = None
        break

    # Ejecutar la opción seleccionada si existe en el diccionario
    if fn in options:
        clear_screen()
        exec(options[fn])
        input("\nPresiona Enter para continuar...")
        clear_screen()
    else:
        print("Error: Opción no válida.")