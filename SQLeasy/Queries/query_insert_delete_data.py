# This is the place where new queries should be implemented. Define a unique
# identifier variable, then copy/paste the function to the configuration
# file.

# POPULATE TABLES
# This query belongs to a table with an "AUTO_INCREMENT" inndex value; remember
# to left 'NULL' the '_id' field.
populate_table = """
INSERT INTO dummy_table VALUES
(NULL, 'Atolon Inc.', 'Address street, 42', 'Rollos de pelicula', 'metrajes a encargo', '666666666', '0'),
(NULL, 'Telas asfalticas NG.', 'Address boulevard, 21', 'Obra publica', 'hoyos/hundimientos', '666000000', '1');
"""

# To push Python data structures(lists of tuples) into a database.
# This construction, isolates the values from the usual query:
# The Query:
insert_multiple_queries = """
  INSERT INTO clients (name, address, industry, location, postal_code, email, notes, telephone, created, client_type, status)
  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

insert_multiple_dummy = """
  INSERT INTO dummy_table (name, address, industry, location, postal_code, email, notes, telephone, created, client_type, status)
  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# DELETE DATA
# When an entire row is deleted from a table, the other index will not be
# affected; but the table will remain with a no-contiguous list of numbered
# indexes.
delete_registry = """
    DELETE FROM dummy_table
    WHERE dummy_id = 1;
"""

# to delete multiple rows, write a line for each one.
# This is not valid '1, 2, 37, 38, 39, 40, 41, 42, 43, 44'

# As a general rule; to overwrite identifiers(whatever_id), is a bad idea.
# Because you are rewriting history! Once a row is deleted, forget the entry.
# SQL has 'methods' enough to not bother with that. Some people enter a
# dummy_row, with a note reffering the deleted entry. Pff, innecessary!;
# but in the worst situation, the dummy_row case it's acceptable.
# Another aproach, is to dump the entire table, 'format' the new data,
# and push the datum again. All information in a table it's precious, and
# should be preserved; like a jump in a counter. Some DataBase administrators
# goes crazy when some unexperienced user, decides to change the counter.
# Counter strikes!
# Do you know that all information in a DataBase it's accounted! it has
# a similar concept as the repo(repository).
delete_multiple = """
    DELETE FROM dummy_table WHERE dummy_id = 1;
    DELETE FROM dummy_table WHERE dummy_id = 2;
    DELETE FROM dummy_table WHERE dummy_id = 3;
"""

################################################
############### TABLE INSERTS ##################
################################################
# client_id, client_name, client_address, client_industry, client_location,
# client_postal_code, client_email, client_notes, client_telephone,
# client_created, client_status
# DATE FOMAT: YYYY-MM-DD hh:mm:ss, or simply refer to now() to match with the actual date.
# POSTAL CODE: This fileld can't start with Zero(0). It's a problem.
insert_clients_table = """
( NULL, 'correcaminos', 'addr', 'indust', 'loc', '08000', 'mail@str', 'notes', 600600600, now(), 1);
"""
# format CURRENT_TIMESTAMP: returns current date and time; YYYY-MM-DD hh:mm:ss.
insert_products = """
( NULL, 'name', '123AA89-99z', 'description', 1.99, 20, 16, 200.42, NULL, 1)
"""

insert_services = """
(NULL, 'name', 12345AA-ff3R, 'description', 17.42, 20, 16, 200.42, 0)
"""

insert_offers = """
(NULL, 10, 'name', 'description', 17.42, 25, 16, 200.17, 1)
"""

insert_budgets = """
(NULL, 10, 'name', 'description', 17.42, 20, 16, 200.42, 0)
"""

insert_bills = """
(NULL, 10, 'name', 'description', 17.42, 20, 16, 200.42, 1)
"""

insert_orders = """
(NULL, 10, 'name', 'description', 17.42, 20, 16, 200.42, 1)
"""

insert_dn = """
(NULL, 10, 'name', 'description', 17.42, 20, 16, 200.42, 1)
"""

