from Queries import query_create_delete_db as db_queries
from Queries import query_create_delete_table as table_queries
from Queries import query_alter_tables_psg as alter_queries
from Queries import query_insert_delete_data as insert_queries
from Queries import query_simple_queries as simple_queries
from Queries import query_update_tables as update_queries
from Queries import query_messages as messages_queries

# This File is a map of known queries. To add new ones, just define a new variable
# and place there your query as a simple string. At the same time, could be
# used as a configuration file.

################################################
################### DEFAULTS ###################
################################################
# DEFAULT DATA BASE
defaultdB = 'customers_db'

# DEFAULT FILE
file = 'birdOfFire.txt'

# VAULT
# Idealy, this path should be an URL path, to the 'vault-tec' server we
# expect to host in an undeterminated future. TécnicoSistema(raulvilchez.org).
vault = '.hatch'

# PANDAS COLUMNS
# It should be consulted the table before; run a simple query to
# get the column's name.
p_columnus = ['client_id', 'client_name', 'client_address', 'client_industry', 'client_notes', 'client_telephone', 'client_status']

################################################
################### QUERIES ###################
################################################

# DEFAULT QUERY
q1 = simple_queries.default_query

# SHOW DATABASES
show = simple_queries.databases

# DATA BASES' NAMES
dbNames = ['customers_db', 'dummy_db', 'postgres', 'information_schema', 
           'pg_catalog']

# CREATE DATABASE
create_db = db_queries.create_db

# DELETE DATABASE
delete_db = db_queries.delete_db

# CREATE TABLE
create_table = table_queries.create_table

# DELETE TABLE
delete_table = table_queries.delete_table

# DELETE MULTIPLE TABLES
delete_multiple_tables = table_queries.delete_multiple_tables

# ALTER TABLES
alter_table = alter_queries.table_alters

# Populate tables
p_table = insert_queries.populate_table

# To update data
update_query = update_queries.update_id

# Delete data
delete_entry = insert_queries.delete_registry

# Insert multiple values
# Do Note, that the placeholder has nothing to do with Python's strings
# data type '%s'. Sql will use this syntax to work with all types
# sql placeholder '%s' --> (str, int, dates...).
# The data structures:
insert_multiple = insert_queries.insert_multiple_queries

val = [
    (7, 'Hunk', 'Dodson', 'ENG', None, '1991-12-23', 11111, '+09812734098'),
    (8, 'Funk', 'Bolson', 'EKR', 'ENG', '1491-15-16', 22222, '+09219014098')
]


################################################
############### APPLICATION MESAGES ############
################################################
msg_map = {
    'message': messages_queries.message,
    'chosedB': messages_queries.chosedB,
    'test_message': messages_queries.test_message,
    'atention': messages_queries.atention,
    'cancel_action': messages_queries.cancel_action,
    'selectDb': messages_queries.selectDb,
    'wrongDb': messages_queries.wrongDb,
    'typeName': messages_queries.typeName
}

for key, value in msg_map.items():
    globals()[key] = value