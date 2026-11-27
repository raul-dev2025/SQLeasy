# This is the place where new queries should be implemented. Define a unique
# identifier variable, then copy/paste the function to the configuration
# file.

# CREATE TABLE
create_table2 = """
    CREATE TABLE dummy_table(
      dummy_id SERIAL PRIMARY KEY,
      dummy_name VARCHAR(40) NOT NULL,
      dummy_address VARCHAR(60) NOT NULL,
      dummy_industry VARCHAR(20),
      dummy_notes VARCHAR(60),
      dummy_telephone INT,
      dummy_status BOOLEAN
    );
"""

# DELETE TABLE
delete_table = """
    DROP TABLE dummy_table
"""

# DELETE MULTIPLE TABLES
delete_multiple_tables = """
    DROP TABLE bills, budgets, clients, delivery_notes, offers, orders, products, services;
"""
