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




        connection.commit()

    except Exception as e:

    finally:

