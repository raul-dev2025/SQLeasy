# Inserción de los datos maestros del cliente
query_cliente = """
    INSERT INTO clients (name, address, industry, location, postal_code, email, notes, telephone, created, client_type, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s)
    RETURNING id;
"""
# Si se aporta un contrato inicial, procesarlo
query_iguala = """
    INSERT INTO iguala (client_id, modalidad, bloque_contratado, horas_incluidas, tarifa_mensual, fecha_inicio, fecha_fin, status, observaciones)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
"""

query_bolsa = """
    INSERT INTO bolsa_horas (client_id, tipo_bolsa, horas_compradas, fecha_caducidad, status)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
"""

# Registrar la relación en la tabla Hub (contratos_cliente)
query_hub = """
    INSERT INTO contratos_cliente (client_id, tipo_servicio, referencia_id, estado, observaciones)
    VALUES (%s, %s, %s, %s, %s);
"""
