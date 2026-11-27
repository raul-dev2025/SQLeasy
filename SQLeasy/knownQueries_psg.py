from Queries import query_create_delete_db as db_queries
from Queries import query_create_delete_table as table_queries
from Queries import query_alter_tables_psg as alter_queries
from Queries import query_insert_delete_data as insert_queries
from Queries import query_simple_queries as simple_queries
from Queries import query_update_tables as update_queries
from Queries import query_messages as messages_queries
from Queries import query_fix_psg as fix_and_bugs
from Queries import query_clientsDB_psg as dbClients
from Tuplas import pymes as myTuple
from Filters import filter_clients_table as names


# This File is a map of known queries. To add new ones, just define a new variable
# and place there your query as a simple string. At the same time, could be
# used as a configuration file.

################################################
################### DEFAULTS ###################
################################################
# DEFAULT DATA BASE
defaultdB = 'None'

# DEFAULT FILE
file = 'birdOfFire.txt'

# VAULT
vault = '.hatch'

# PANDAS COLUMNS
p_columnus = ['id', 'name', 'address', 'industry', 'location', 'postal_code', 'email', 'notes', 'telephone', 'created', 'client_type', 'status']

################################################
################### QUERIES ###################
################################################

# Default query. LIBRERÍA: query_simple_queries
q1 = simple_queries.default_query

# SHOW DATABASES
show = simple_queries.user_databases

# DATA BASES' NAMES
# dbNames = ['customers_db', 'dummy_db', 'postgres', 'information_schema', 'pg_catalog']

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
orders_alter = alter_queries.orders_alters

# Populate tables. LIBRERÍA: query_insert_delete_data
p_table = insert_queries.populate_table

# Delete data. LIBRERÍA: query_insert_delete_data
delete_entry = insert_queries.delete_registry

# Insert multiple values. LIBRERÍA: query_insert_delete_data
insert_multiple = insert_queries.insert_multiple_queries

# To update data. LIBRERÍA: query_update_tables
update_query = update_queries.update_id

# Fix and bugs. LIBRERÍA: query_fix_psg
fix_entry = fix_and_bugs.fix_id

# LIBRERÍA: Tuplas
val = myTuple.val

# Filters LIBRARY: Filters
repeated_names = names.name_matching

################################################
############### APPLICATION MESAGES ############
################################################
msg_map = {
    'init_app': messages_queries.init_app,
    'message': messages_queries.message,
    'chosedB': messages_queries.chosedB,
    'test_message': messages_queries.test_message,
    'atention': messages_queries.atention,
    'cancel_action': messages_queries.cancel_action,
    'selectDb': messages_queries.selectDb,
    'wrongDb': messages_queries.wrongDb,
    'fail_con': messages_queries.connection_failed,
    'typeName': messages_queries.typeName
}

for key, value in msg_map.items():
    globals()[key] = value