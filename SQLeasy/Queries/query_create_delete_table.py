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

create_table = """
    CREATE TABLE dummy_table(
      id SERIAL PRIMARY KEY,
      name VARCHAR(100) NOT NULL,
      address VARCHAR(100) NOT NULL,
      industry VARCHAR(40),
      location VARCHAR(40),
      postal_code VARCHAR(10),
      email VARCHAR(100),
      notes VARCHAR(500),
      telephone VARCHAR(20),
      created TIMESTAMP NOT NULL,
      client_type VARCHAR(30),
      status BOOLEAN NOT NULL DEFAULT FALSE
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
