========================
Plan de trabajo acordado
========================


1. **Esquema de `dummy_table`, `p_columnus` y estructura de `val`:** alinear los nombres de columna de la tabla (`id`, `name`, `address`, `industry`, `location`, `postal_code`, `email`, `notes`, `telephone`, `created`, `client_type`, `status`) con `p_columnus` y definir cómo mapear o indexar cada campo de las tuplas en `val` (donde falta `id`) de forma segura y clara.
2. **Consulta de lectura en `Queries/` y `knownQueries_psg.py`:** definir la consulta `SELECT` contra `dummy_table` en el módulo correspondiente de `Queries/` y mapearla en `knownQueries_psg.py` para leer mediante `FreeCC_psg.read_query`.
3. **Funciones de normalización (`normalize_text` y `normalize_email`):** diseñar la lógica de limpieza y validación de texto y correos (incluyendo marcadores no válidos) antes de comparar.
4. **Función de detección de duplicados (`find_duplicates`):** definir la lógica de cruce entre las tuplas candidatas de `val` y los registros existentes de `dummy_table` (por nombre, email o ambos), evitando dependencias frágiles de índices mágicos.
5. **Salida y reporte del filtro:** decidir cómo presentar los duplicados (consola, archivo de log o ambos) y cómo estructurar la función que formatea o emite los resultados.
6. **Integración en `data_ops.py`, `query_messages.py` y flujo de ejecución:** conectar la operación en `data_ops.py`, actualizar `message` en `query_messages.py` reemplazando `0. List saved queries` por la nueva opción y revisar cómo se invoca desde el menú.


Punto 1: Esquema de `dummy_table`, `p_columnus` y estructura de `val`
=====================================================================


En `dummy_table` tenemos 12 columnas: `id` (auto-incremental `SERIAL`), seguida de 11 campos de datos: `name`, `address`, `industry`, `location`, `postal_code`, `email`, `notes`, `telephone`, `created`, `client_type` y `status`. En `knownQueries_psg.py`, `p_columnus` ya lista esos 12 nombres en ese mismo orden.

Como en `val` las tuplas omiten `id` y funcionan como filas posicionales (tipo CSV/registro sin PK), hay dos formas limpias de referenciar sus campos sin depender de índices sueltos esparcidos por el código:

* Definir un mapa o constante de índices/columnas para las tuplas de `val` (por ejemplo, asociando cada nombre de campo de `dummy_table` —excluyendo `id`— con su posición en la tupla) o desempaquetar/leer mediante un helper que busque por nombre de columna.
* Al leer de PostgreSQL con `FreeCC_psg.read_query`, podemos pedir explícitamente las columnas necesarias (por ejemplo, `id, name, email` o las que definamos en el filtro) y asociar cada fila a su nombre de columna usando `p_columnus` o el orden del `SELECT`, para no depender tampoco de posiciones fijas en la lógica de comparación.

Antes de pasar al **Punto 2** (la consulta en `Queries/` y su mapeo en `knownQueries_psg.py`), ¿qué campos exactos de `val` y de `dummy_table` quieres usar como criterio de duplicado (por ejemplo `name` y `email`, o alguno más) y qué posición ocupa cada uno en las tuplas actuales de `val`?