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
# one to many: one product to many clients!
# If you want to know which product belongs to which provaider
# you must start a query aginst the provaiderDB. So product_sku_num
# is the key here.
# Tabla del catálogo de productos
create_products_table = """
    CREATE TABLE products(
      id SERIAL PRIMARY KEY,
      product_name VARCHAR(40) NOT NULL,
      product_sku_num VARCHAR(20) NOT NULL,
      product_description VARCHAR(60) NOT NULL,
      product_price decimal,
      product_discount INT,
      product_tax INT,
      product_pvp decimal,
      product_last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      status BOOLEAN NOT NULL DEFAULT FALSE
    );
"""

# Tabla de servicios disponibles
create_services_table = """
    CREATE TABLE services(
      id SERIAL PRIMARY KEY,
      service_name VARCHAR(40) NOT NULL,
      product_sku_num VARCHAR(20) NOT NULL,
      service_description VARCHAR(60) NOT NULL,
      service_price decimal,
      service_discount INT,
      service_tax INT,
      service_pvp decimal,
      service_last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      status BOOLEAN NOT NULL DEFAULT FALSE
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
      id SERIAL PRIMARY KEY,
      client_id INT DEFAULT NULL,
      offer_name VARCHAR(40) NOT NULL,
      offer_description VARCHAR(60) NOT NULL,
      offer_price decimal,
      offer_discount INT,
      offer_tax INT,
      offer_pvp decimal,
      offer_last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      status BOOLEAN NOT NULL DEFAULT FALSE,
      FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL
    );
"""

# Tabla de presupuestos
create_budgets_table = """
    CREATE TABLE budgets(
      id SERIAL PRIMARY KEY,
      client_id INT DEFAULT NULL,
      budget_name VARCHAR(40) NOT NULL,
      budget_description VARCHAR(60) NOT NULL,
      budget_price decimal,
      budget_discount INT,
      budget_tax INT,
      budget_pvp decimal,
      offer_last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      status BOOLEAN NOT NULL DEFAULT FALSE,
      FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL
    );
"""

# Tabla de facturación(facturas)
create_bills_table = """
    CREATE TABLE bills(
      id SERIAL PRIMARY KEY,
      client_id INT DEFAULT NULL,
      bill_name VARCHAR(40) NOT NULL,
      bill_description VARCHAR(60) NOT NULL,
      bill_price decimal,
      bill_discount INT,
      bill_tax INT,
      bill_pvp decimal,
      offer_last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      status BOOLEAN NOT NULL DEFAULT FALSE,
      FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL
    );
"""

# Tabla de pedidos
create_orders_table = """
    CREATE TABLE orders(
      id SERIAL PRIMARY KEY,
      client_id INT DEFAULT NULL,
      order_name VARCHAR(40) NOT NULL,
      order_description VARCHAR(60) NOT NULL,
      order_price decimal,
      order_discount INT,
      order_tax INT,
      order_pvp decimal,
      offer_last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      status BOOLEAN NOT NULL DEFAULT FALSE,
      FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL
    );
"""

# Tabla de albaranes de entrega
create_delivery_notes_table = """
    CREATE TABLE delivery_notes(
      id SERIAL PRIMARY KEY,
      client_id INT DEFAULT NULL,
      dn_name VARCHAR(40) NOT NULL,
      dn_description VARCHAR(60) NOT NULL,
      dn_price decimal,
      dn_discount INT,
      dn_tax INT,
      dn_pvp decimal,
      offer_last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      status BOOLEAN NOT NULL DEFAULT FALSE,
      FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE SET NULL
    );
"""

# Tabla de control de bolsa de horas y consumo de saldo
create_hourly_pool_table = """
    CREATE TABLE bolsa_horas (
      id SERIAL PRIMARY KEY,
      client_id INT NOT NULL,
      tipo_bolsa INT NOT NULL CHECK (tipo_bolsa IN (10, 25, 50, 100)),
      horas_compradas NUMERIC(6,2) NOT NULL,
      horas_consumidas NUMERIC(6,2) DEFAULT 0.00,
      horas_restantes NUMERIC(6,2) GENERATED ALWAYS AS (horas_compradas - horas_consumidas) STORED,
      fecha_caducidad DATE NOT NULL,
      status BOOLEAN DEFAULT FALSE,
      fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
    );
"""

# Tabla Hub central para asociar cualquier tipo de servicio/contrato al cliente
create_client_contracts = """
    CREATE TABLE contratos_cliente (
      id SERIAL PRIMARY KEY,
      client_id INT NOT NULL,
      tipo_servicio VARCHAR(30) NOT NULL CHECK (tipo_servicio IN ('iguala_programada', 'iguala_indefinida', 'bolsa_horas', 'intervencion_ad_hoc')),
      referencia_id INT NOT NULL,
      estado VARCHAR(20) DEFAULT 'activo' CHECK (estado IN ('activo', 'pausado', 'finalizado', 'renovado')),
      fecha_alta TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      observaciones TEXT,
      FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
    );
"""

# Tabla de registro de intervenciones técnicas presenciales o remotas
create_interventions_table = """
    CREATE TABLE intervenciones (
      id SERIAL PRIMARY KEY,
      client_id INT NOT NULL,
      contrato_cliente_id INT DEFAULT NULL,
      tipo_actuacion VARCHAR(30) CHECK (tipo_actuacion IN ('presencial', 'remota')),
      fecha_intervencion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      descripcion TEXT NOT NULL,
      horas_reales_invertidas NUMERIC(5,2) NOT NULL,
      horas_descontadas_o_facturadas NUMERIC(5,2) NOT NULL,
      es_exceso BOOLEAN DEFAULT FALSE,
      status BOOLEAN NOT NULL DEFAULT FALSE,
      FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
      FOREIGN KEY (contrato_cliente_id) REFERENCES contratos_cliente(id) ON DELETE SET NULL
    );
"""

# Tabla de contratos de iguala y condiciones periódicas
create_maintenance_contract_table = """
    CREATE TABLE iguala (
      id SERIAL PRIMARY KEY,
      client_id INT NOT NULL,
      modalidad VARCHAR(30) NOT NULL CHECK (modalidad IN ('programada', 'indefinida')),
      bloque_contratado VARCHAR(30) NOT NULL CHECK (bloque_contratado IN ('base_2h', 'estandar_5h', 'avanzado_10h')),
      horas_incluidas NUMERIC(5,2) NOT NULL,
      tarifa_mensual NUMERIC(10,2) NOT NULL,
      fecha_inicio DATE NOT NULL,
      fecha_fin DATE,
      status BOOLEAN DEFAULT FALSE,
      observaciones TEXT,
      FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
    );
"""

# Tabla de gestión de avisos y urgencias prioritarias
create_emergencies_table = """
    CREATE TABLE urgencias (
      id SERIAL PRIMARY KEY,
      client_id INT NOT NULL,
      intervencion_id INT DEFAULT NULL,
      fecha_aviso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      nivel_prioridad VARCHAR(20) CHECK (nivel_prioridad IN ('Alta', 'Critica', 'Urgente')),
      descripcion_incidencia TEXT NOT NULL,
      tiempo_respuesta_minutos INT,
      resuelta BOOLEAN DEFAULT FALSE,
      FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE,
      FOREIGN KEY (intervencion_id) REFERENCES intervenciones(id) ON DELETE SET NULL
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
( NULL, 'correcaminos', 'addr', 'indust', 'loc', '08000', 'mail@str', 'notes', 600600600, now(), 1);
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
