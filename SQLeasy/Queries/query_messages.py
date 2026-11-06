################################################
############### APPLICATION MESAGES ############
################################################
message = """
You can do the following actions:
      1. Test connection        5. ConnectionDB         9. Insert into Table
      2. Start a new query      6. List Databases       10. Erase from Table
      3. Create DataBase        7. Create Table         11. Python structures
      4. Delete DataBase        8. Delete Table         12. Dump Html
                q. Exit                         0. List saved queries
"""

chosedB = """
Type the Data Base to update the SQL command
or chose one in the list:\n{}"""

test_message = """
    This is a test message with formated text, ready to get displayed \
    by the namespace.
"""

atention = """
ATENTION! This action can NOT be UNDONE. \
Do you want to proceed?
"""

cancel_action = """
The process "delete_db" was canceled.
"""

selectDb = """
      Chose one of the available Databases first
      by typing one, from the following list.
      If the Database does not exist, create one before this action.
"""

wrongDb = """
\tError; The database you typed it does not exist.\n \
\tCreate one or choose another !
"""

typeName = """
\tWrite the DataBase name:
"""