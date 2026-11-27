# DEFAULT QUERY
default_query = """
    SELECT *
    FROM clients
"""

databases = """
    SELECT datname
    FROM pg_database
    WHERE datistemplate = false;
"""

user_databases = """
    SELECT datname
    FROM pg_database
    WHERE datistemplate = false
    AND datname NOT IN (
      'autoupdate',
      'mediaserver',
      'ong',
      'synosnmp',
      'synophoto',
      'video_metadata',
      'synoindex',
      'download',
      'mediaserver_ascii'
    )
    ORDER BY datname;
"""

# FILTERING DATABASES LIST, using SHOW DATABASES LIKE
#    SHOW {DATABASES | SCHEMAS}
#    [LIKE 'pattern' | WHERE expression]
# This shows all databases that start with 's'.
filtering = """
    SHOW DATABASES like 's%';
"""
# SHOW DATABASES
sel_scheme = """
SELECT scheme_name
FROM information_scheme.schemetab;
"""
# CURRENT DATABASE
# It will not show anythng if a database it's not chosen before.
currentDb = """
SELECT DATABASE();
"""
# SHOW TABLES
# It will not show anythng if a database it's not chosen before.
show_tables = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'public';
"""

show_table = """
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'clients';
"""

# query JOIN
q5 = """
    SELECT course.course_id, course.course_name, course.course_language, client.client_name, client.client_address
    FROM course
    JOIN client
    ON course.client = client.client_id
    WHERE course.in_school = FALSE;
"""

q6 = """
    SELECT id, name, status FROM clients;
"""

pendientes = """
    SELECT
      id,
      name,
      CONCAT_WS(
        ', ',
        CASE WHEN LOWER(TRIM(address)) = 'pendiente' THEN 'address' END,
        CASE WHEN LOWER(TRIM(industry)) = 'pendiente' THEN 'industry' END,
        CASE WHEN LOWER(TRIM(location)) = 'pendiente' THEN 'location' END,
        CASE WHEN LOWER(TRIM(postal_code)) = 'pendiente' THEN 'postal_code' END,
        CASE WHEN LOWER(TRIM(email)) = 'pendiente' THEN 'email' END,
        CASE WHEN LOWER(TRIM(notes)) = 'pendiente' THEN 'notes' END,
        CASE WHEN LOWER(TRIM(telephone)) = 'pendiente' THEN 'telephone' END,
        CASE WHEN LOWER(TRIM(client_type)) = 'pendiente' THEN 'client_type' END
      ) AS campos_pendientes
    FROM clients
    WHERE
      LOWER(TRIM(name)) = 'pendiente'
      OR LOWER(TRIM(address)) = 'pendiente'
      OR LOWER(TRIM(industry)) = 'pendiente'
      OR LOWER(TRIM(location)) = 'pendiente'
      OR LOWER(TRIM(postal_code)) = 'pendiente'
      OR LOWER(TRIM(email)) = 'pendiente'
      OR LOWER(TRIM(notes)) = 'pendiente'
      OR LOWER(TRIM(telephone)) = 'pendiente'
"""

