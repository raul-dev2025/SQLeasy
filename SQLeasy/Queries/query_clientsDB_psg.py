# 1. Place an import for this file, i.e: import Queries.name
#    Remember, Python uses selectors to access vars and funcs.
#         <name.name> correct
#         <name/name> wrong!
# 2. Connection could be reused -it should be a delay to resset any valid one,
#    but it's needed to add a new call for each query, i.e:
#    connection = my_awesomeConn_fn()
#    fn_name(connection, sql_var)
#    fn_name(connection, sql_var)
#    ...
# 3. The easiest thing is to avoid innecessary imports, and just use the configuration
#    file. Remember to flush all extra calls from code, to keep it clean.

# client_id, client_name, client_address, client_industry, client_location,
# client_postal_code, client_email, client_notes, client_telephone,
# client_created, client_status
# Tabla principal de clientes y datos de contacto
create_clients_table = """
    CREATE TABLE clients(
      client_id SERIAL PRIMARY KEY,
      client_name VARCHAR(40) NOT NULL,
      client_address VARCHAR(60) NOT NULL,
      client_industry VARCHAR(20),
      client_location VARCHAR(20),
      client_postal_code INT,
      client_email VARCHAR(20),
      client_notes VARCHAR(60),
      client_telephone INT,
      client_created TIMESTAMP NOT NULL,
      client_status BOOLEAN NOT NULL DEFAULT TRUE
    );
"""
# one to many: one product to many clients!
# If you want to know which product belongs to which provaider
# you must start a query aginst the provaiderDB. So product_sku_num
# is the key here.
# Tabla del catálogo de productos
create_products_table = """
    CREATE TABLE products(
      product_id SERIAL PRIMARY KEY,
      product_name VARCHAR(40) NOT NULL,
      product_sku_num VARCHAR(20) NOT NULL,
      product_description VARCHAR(60) NOT NULL,
      product_price decimal,
      product_discount INT,
      product_tax INT,
      product_pvp decimal,
      product_last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      product_status BOOLEAN NOT NULL DEFAULT TRUE
    );
"""

# Tabla de servicios disponibles
create_services_table = """
    CREATE TABLE services(
      service_id SERIAL PRIMARY KEY,
      service_name VARCHAR(40) NOT NULL,
      product_sku_num VARCHAR(20) NOT NULL,
      service_description VARCHAR(60) NOT NULL,
      service_price decimal,
      service_discount INT,
      service_tax INT,
      service_pvp decimal,
      service_last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      service_status BOOLEAN NOT NULL DEFAULT TRUE
    );
"""

# When it's needed to relate some table, that is; to reference
# a table field from an external table, the column name that
# recives the 'foreign key' IT MUST EXIST, before stablish
# the cross reference. In this case it's wanted to reference
# the client table, so it is added a client field on each table.
# Tabla de ofertas comerciales vinculadas a clientes
create_offers_table = """
    CREATE TABLE offers(
      offer_id SERIAL PRIMARY KEY,
      client INT DEFAULT NULL,
      offer_name VARCHAR(40) NOT NULL,
      offer_description VARCHAR(60) NOT NULL,
      offer_price decimal,
      offer_discount INT,
      offer_tax INT,
      offer_pvp decimal,
      offer_last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      offer_status BOOLEAN NOT NULL DEFAULT TRUE
    );
"""

# Tabla de presupuestos
create_budgets_table = """
    CREATE TABLE budgets(
      budget_id SERIAL PRIMARY KEY,
      client INT DEFAULT NULL,
      budget_name VARCHAR(40) NOT NULL,
      budget_description VARCHAR(60) NOT NULL,
      budget_price decimal,
      budget_discount INT,
      budget_tax INT,
      budget_pvp decimal,
      offer_last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      budget_status BOOLEAN NOT NULL DEFAULT TRUE
    );
"""

# Tabla de facturación(facturas)
create_bills_table = """
    CREATE TABLE bills(
      bill_id SERIAL PRIMARY KEY,
      client INT DEFAULT NULL,
      bill_name VARCHAR(40) NOT NULL,
      bill_description VARCHAR(60) NOT NULL,
      bill_price decimal,
      bill_discount INT,
      bill_tax INT,
      bill_pvp decimal,
      offer_last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      bill_status BOOLEAN NOT NULL DEFAULT TRUE
    );
"""

# Tabla de pedidos
create_orders_table = """
    CREATE TABLE orders(
      order_id SERIAL PRIMARY KEY,
      client INT DEFAULT NULL,
      order_name VARCHAR(40) NOT NULL,
      order_description VARCHAR(60) NOT NULL,
      order_price decimal,
      order_discount INT,
      order_tax INT,
      order_pvp decimal,
      offer_last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      order_status BOOLEAN NOT NULL DEFAULT TRUE
    );
"""

# Tabla de albaranes de entrega
create_delivery_notes_table = """
    CREATE TABLE delivery_notes(
      dn_id SERIAL PRIMARY KEY,
      client INT DEFAULT NULL,
      dn_name VARCHAR(40) NOT NULL,
      dn_description VARCHAR(60) NOT NULL,
      dn_price decimal,
      dn_discount INT,
      dn_tax INT,
      dn_pvp decimal,
      offer_last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      dn_status BOOLEAN NOT NULL DEFAULT TRUE
    );
"""

# Tabla de control de bolsa de horas y consumo de saldo
create_hourly_pool_table = """
    CREATE TABLE bolsa_horas (
      id SERIAL PRIMARY KEY,
      iguala_id INT REFERENCES iguala(id) ON DELETE CASCADE,
      horas_compradas NUMERIC(6,2) NOT NULL,
      horas_consumidas NUMERIC(6,2) DEFAULT 0.00,
      horas_restantes NUMERIC(6,2) GENERATED ALWAYS AS (horas_compradas - horas_consumidas) STORED,
      periodo_mes INT NOT NULL,
      periodo_anio INT NOT NULL,
      fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

# Tabla de registro de intervenciones técnicas presenciales o remotas
create_interventions_table = """
    CREATE TABLE intervenciones(
      intervencion_id SERIAL PRIMARY KEY,
      client INT DEFAULT NULL,
      bolsa_id INT DEFAULT NULL,
      fecha_intervencion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      descripcion VARCHAR(100) NOT NULL,
      horas_invertidas DECIMAL NOT NULL,
      intervencion_status BOOLEAN NOT NULL DEFAULT TRUE
    );
"""

# Tabla de contratos de iguala y condiciones periódicas
create_maintenance_contract_table = """
    CREATE TABLE iguala (
      id SERIAL PRIMARY KEY,
      cliente_id INT NOT NULL,
      concepto VARCHAR(150) NOT NULL,
      horas_incluidas NUMERIC(5,2) DEFAULT 0.00,
      tarifa_mensual NUMERIC(10,2) NOT NULL,
      fecha_inicio DATE NOT NULL,
      fecha_fin DATE,
      activo BOOLEAN DEFAULT TRUE,
      observaciones TEXT
    );
"""

# Tabla de gestión de avisos y urgencias prioritarias
create_emergencies_table = """
    CREATE TABLE urgencias (
      id SERIAL PRIMARY KEY,
      cliente_id INT NOT NULL,
      fecha_aviso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      nivel_prioridad VARCHAR(20) CHECK (nivel_prioridad IN ('Alta', 'Crítica', 'Urgente')),
      descripcion_incidencia TEXT NOT NULL,
      tiempo_respuesta_minutos INT,
      resuelta BOOLEAN DEFAULT FALSE,
      intervencion_asociada_id INT REFERENCES intervenciones(id) ON DELETE SET NULL
    );
"""



################################################
############### TABLE INSERTS ##################
################################################
# client_id, client_name, client_address, client_industry, client_location,
# client_postal_code, client_email, client_notes, client_telephone,
# client_created, client_status
# DATE FOMAT: YYYY-MM-DD hh:mm:ss, or simply refer to now() to match with the actual date.
# POSTAL CODE: This fileld can't start with Zero(0). It's a problem.
insert_clients_table = """
( NULL, 'name', 'addr', 'indust', 'loc', 08000, 'mail@str', 'notes', 6006060, now(), 1);
"""
# format CURRENT_TIMESTAMP: returns current date and time; YYYY-MM-DD hh:mm:ss.
insert_products = """
( NULL, 'name', '123AA89-99z', 'description', 1.99, 20, 16, 200.42, NULL, 1)
"""

insert_services = """
(NULL, 'name', 12345AA-ff3R, 'description', 17.42, 20, 16, 200.42, 0)
"""

insert_offers = """
(NULL, 10, 'name', 'description', 17.42, 25, 16, 200.17, 1)
"""

insert_budgets = """
(NULL, 10, 'name', 'description', 17.42, 20, 16, 200.42, 0)
"""

insert_bills = """
(NULL, 10, 'name', 'description', 17.42, 20, 16, 200.42, 1)
"""

insert_orders = """
(NULL, 10, 'name', 'description', 17.42, 20, 16, 200.42, 1)
"""

insert_dn = """
(NULL, 10, 'name', 'description', 17.42, 20, 16, 200.42, 1)
"""
