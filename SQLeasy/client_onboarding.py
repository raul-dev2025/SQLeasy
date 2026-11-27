from pg_errors import handle_pg_error
from query_alta_cliente import query_client, update_client, insert_client_onboarding

LONGITUD_TUPLA_ALTA = 14
INDICE_CORTE_ALTA = 10

def preparar_datos_de_alta(registro):
  """
  Extrae y valida una tupla de 14 elementos y la divide en los parámetros
  correspondientes a `clients` (10) y `alta_cliente` (4).
  """

  return params_cliente, params_alta

def registrar_alta_cliente(connection, datos_cliente, datos_alta, client_id=None):
    """
    Formaliza el alta de un cliente (nuevo o existente) y registra la entrada
    en alta_cliente dentro de una misma transacción.
    """
    cursor = connection.cursor()
    last_sql = None
    last_params = None

    try:
        parametros_cliente = (
            datos_cliente["name"],
            datos_cliente["address"],
            datos_cliente.get("industry"),
            datos_cliente.get("location"),
            datos_cliente.get("postal_code"),
            datos_cliente.get("email"),
            datos_cliente.get("notes"),
            datos_cliente.get("telephone"),
            datos_cliente.get("client_type"),
            datos_cliente.get("status", True),
        )

        if client_id is not None:
            last_sql = update_client
            last_params = (*parametros_cliente, client_id)
            cursor.execute(last_sql, last_params)
            fila_cliente = cursor.fetchone()
            if not fila_cliente:
                raise ValueError(f"No existe un cliente con id={client_id}")
            resolved_client_id = fila_cliente[0]
        else:
            last_sql = query_client
            last_params = parametros_cliente
            cursor.execute(last_sql, last_params)
            resolved_client_id = cursor.fetchone()[0]

        last_sql = insert_client_onboarding
        last_params = (
            resolved_client_id,
            datos_alta["tipo_servicio"],
            datos_alta["referencia"],
            datos_alta.get("estado", "activo"),
            datos_alta.get("observaciones"),
        )
        cursor.execute(last_sql, last_params)
        alta_id = cursor.fetchone()[0]

        connection.commit()
        return {
            "success": True,
            "client_id": resolved_client_id,
            "alta_id": alta_id,
        }

    except Exception as e:
        diagnostico = handle_pg_error(
            e,
            connection=connection,
            sql=last_sql,
            val=last_params,
            rollback=True,
        )
        raise RuntimeError(f"Error en el alta de cliente -> {diagnostico}") from e

    finally:
        cursor.close()

