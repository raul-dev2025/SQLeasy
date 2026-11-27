from pg_errors import handle_pg_error
from query_alta_cliente import query_client, update_client, insert_client_onboarding


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



        connection.commit()

    except Exception as e:

    finally:

