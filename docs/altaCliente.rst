============
Alta cliente
============


1. Resumen de los puntos tratados para integrar "Alta de cliente"
=================================================================

Estos son los acuerdos y lineamientos definidos hasta ahora para el proceso de alta de cliente:

* **Unidad de ejecución:** el alta opera sobre un único registro (un cliente cada vez) en cada ejecución.
* **Comprobación previa de existencia:** se reutilizará la lógica ya construida del filtro de duplicados para comprobar si el cliente ya existe en `clients` (por coincidencia de nombre y/o email) y obtener su `id` si está presente.
* **Si el cliente NO existe:** se inserta en `clients` con `status` activo (`True`) y la fecha automatizada del alta (`CURRENT_TIMESTAMP`).
* **Si el cliente YA existe:** se actualizan sus datos con los valores aportados en el alta, se pasa `status` a `True` y se actualiza la fecha con `CURRENT_TIMESTAMP`, **conservando su `id` original** para mantener la trazabilidad y la información asociada a ese identificador.
* **Registro en el hub (`contratos_cliente`):** en el momento del alta el cliente siempre debe quedar reflejado en `contratos_cliente` indicando su tipo/condición de cliente, tanto si contrata una modalidad de mantenimiento (como iguala o bolsa de horas) como si no contrata ninguna.
* **Relación con `Tuplas/pymes.py`:** funciona como entrada/bandeja donde se pegan las tuplas prospectadas con el formato esperado para leer desde ahí y llevar a cabo el proceso.


2. Impacto en el módulo actual (`client_onboarding.py` y `query_alta_cliente.py`) y aplicación de cambios
=========================================================================================================

Sí sabemos cómo afecta al módulo actual, y **sí se puede adaptar** para ajustarlo a lo acordado, aunque con una precisión importante sobre los cambios en código:

* **Qué encaja ya y qué cambia en `client_onboarding.py`:**

   * Actualmente `registrar_cliente_con_contrato` siempre hace `INSERT INTO clients` sin comprobar si ya existe ni hacer `UPDATE` conservando `id`, y además solo inserta en `contratos_cliente` cuando entra en las ramas de `iguala_*` o `bolsa_horas` y obtiene `referencia_id`.

* Para ajustarlo al punto 1, el flujo debe comprobar primero si el cliente ya existe (reutilizando el filtro de duplicados), ejecutar `INSERT` o `UPDATE` sobre `clients` (manteniendo el `id` existente y actualizando `created` con `CURRENT_TIMESTAMP`), y registrar siempre una entrada en `contratos_cliente` incluso cuando no haya mantenimiento contratado.

* **Limitación actual de información sobre `contratos_cliente` y el filtro:**

   * En las capturas vistas no tenemos aún la definición exacta de las columnas/valores esperados en `contratos_cliente` cuando **no** hay contrato de mantenimiento (por ejemplo, qué valor lleva `tipo_servicio` o `referencia_id` si es `NULL` o un tipo de alta base), ni la firma exacta con la que invocarás el filtro de duplicados desde `client_onboarding.py`.
   * Tampoco se debe mostrar código fuente completo sin confirmación previa tras discutir la lógica.

Podemos definir ahora mismo la lógica exacta de esos dos puntos (cómo se invoca el filtro para obtener el `id` existente y qué valores recibe `contratos_cliente` sin mantenimiento) y, una vez acordada la lógica, te pido confirmación para aplicar o mostrar los cambios en el módulo.

¿Confirmas cómo quieres tratar el registro en `contratos_cliente` cuando no hay mantenimiento (por ejemplo, con `referencia_id` en `None` y un `tipo_servicio` concreto) para cerrar el diseño antes de pasar al siguiente punto?