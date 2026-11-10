fix_id = """
    SELECT setval(pg_get_serial_sequence('clients', 'id'), COALESCE(MAX(id), 1)) FROM clients;
"""

warning_id = """
    -- Paso 1: Desplazar temporalmente todos los IDs fuera del rango usando un offset alto
    UPDATE clients SET id = id + 10000;

    -- Paso 2: Asignar los IDs definitivos ordenados correlativamente del 1 en adelante
    WITH numbered_clients AS (
        SELECT id, ROW_NUMBER() OVER (ORDER BY created, id) as new_id
        FROM clients
    )
    UPDATE clients
    SET id = numbered_clients.new_id
    FROM numbered_clients
    WHERE clients.id = numbered_clients.id;
"""
