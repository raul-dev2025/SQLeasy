# Inserción de los datos maestros del cliente
query_client = """
    INSERT INTO clients (name, address, industry, location, postal_code, email, notes, telephone, created, client_type, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s)
    RETURNING id;
"""

update_client = """
UPDATE clients
SET
    name = %s,
    address = %s,
    industry = %s,
    location = %s,
    postal_code = %s,
    email = %s,
    notes = %s,
    telephone = %s,
    client_type = %s,
    status = %s
WHERE id = %s
RETURNING id;
"""

# Registrar la relación en la tabla Hub (contratos_cliente)
query_hub = """
    INSERT INTO contratos_cliente (client_id, tipo_servicio, referencia_id, estado, observaciones)
    VALUES (%s, %s, %s, %s, %s);
"""
