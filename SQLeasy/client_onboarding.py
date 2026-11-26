from query_alta_cliente import query_cliente, query_iguala, query_bolsa, query_hub

def registrar_cliente_con_contrato(connection, datos_cliente, datos_contrato=None):
    """
    Registra un cliente de forma transaccional y, opcionalmente, 
    su contrato inicial asociado vinculándolo a través del Hub (contratos_cliente).
    """
    cursor = connection.cursor()
    try:
        # Paso 1: Inserción de los datos maestros del cliente
        cursor.execute(query_cliente, (
            datos_cliente['name'],
            datos_cliente['address'],
            datos_cliente.get('industry'),
            datos_cliente.get('location'),
            datos_cliente.get('postal_code'),
            datos_cliente.get('email'),
            datos_cliente.get('notes'),
            datos_cliente.get('telephone'),
            datos_cliente.get('client_type'),
            datos_cliente.get('status', True)
        ))
        client_id = cursor.fetchone()[0]

        # Paso 2 y 3: Si se aporta un contrato inicial, procesarlo
        if datos_contrato:
            tipo_servicio = datos_contrato['tipo_servicio']
            referencia_id = None

            if tipo_servicio in ('iguala_programada', 'iguala_indefinida'):
                cursor.execute(query_iguala, (
                    client_id,
                    datos_contrato['modalidad'],
                    datos_contrato['bloque_contratado'],
                    datos_contrato['horas_incluidas'],
                    datos_contrato['tarifa_mensual'],
                    datos_contrato['fecha_inicio'],
                    datos_contrato.get('fecha_fin'),
                    datos_contrato.get('status', True),
                    datos_contrato.get('observaciones')
                ))
                referencia_id = cursor.fetchone()[0]

            elif tipo_servicio == 'bolsa_horas':
                cursor.execute(query_bolsa, (
                    client_id,
                    datos_contrato['tipo_bolsa'],
                    datos_contrato['horas_compradas'],
                    datos_contrato['fecha_caducidad'],
                    datos_contrato.get('status', True)
                ))
                referencia_id = cursor.fetchone()[0]

            # Paso 4: Registrar la relación en la tabla Hub (contratos_cliente)
            if referencia_id:
                cursor.execute(query_hub, (
                    client_id,
                    tipo_servicio,
                    referencia_id,
                    datos_contrato.get('estado', 'activo'),
                    datos_contrato.get('observaciones')
                ))

        # Consolidar la transacción si todo ha ido bien
        connection.commit()
        return {"success": True, "client_id": client_id}

    except Exception as e:
        # Revertir cambios en caso de error para mantener la integridad
        connection.rollback()
        raise RuntimeError(f"Error en el alta transaccional del cliente: {e}")

    finally:
        cursor.close()