# Conceptos Fundamentales de Bases de Datos: SQL y DDL

## 1. ¿Qué es SQL?

**SQL** son las siglas de **Structured Query Language** (Lenguaje de Consulta Estructurado). Es el lenguaje estándar universal utilizado para **comunicarse, interactuar y administrar bases de datos relacionales** (como PostgreSQL, MySQL, SQL Server, Oracle, SQLite, entre otras).

A diferencia de los lenguajes de programación tradicionales (como Python o C), SQL es un lenguaje declarativo orientado a conjuntos: le indicas a la base de datos **qué** quieres obtener o hacer, y el motor de la base de datos se encarga de decidir **cómo** hacerlo de forma eficiente.

### ¿Para qué sirve SQL?
Permite realizar cualquier operación sobre la información almacenada en tablas estructuradas en filas y columnas. Sus funciones principales se dividen en varios sublenguajes:

1. **DDL (Data Definition Language):** Para definir y modificar la estructura (tablas, esquemas, índices). Ejemplos: `CREATE`, `ALTER`, `DROP`.
2. **DML (Data Manipulation Language):** Para gestionar los datos dentro de las tablas (consultar, insertar, actualizar, borrar). Ejemplos: `SELECT`, `INSERT`, `UPDATE`, `DELETE`.
3. **DCL (Data Control Language):** Para controlar la seguridad y los permisos de acceso de los usuarios. Ejemplos: `GRANT`, `REVOKE`.
4. **TCL (Transaction Control Language):** Para gestionar transacciones y asegurar la integridad de los datos. Ejemplos: `COMMIT`, `ROLLBACK`.

### Ejemplo práctico de SQL (Consulta DML)
Una consulta típica para obtener los nombres y correos de los usuarios activos de una tabla sería:

```sql
SELECT nombre, correo 
FROM usuarios 
WHERE activo = true;
```

---

## 2. ¿Qué significa DDL?

En el contexto de SQL y las bases de datos relacionales, **DDL** son las siglas de **Data Definition Language** (Lenguaje de Definición de Datos).

Es el subconjunto de instrucciones SQL utilizado para **definir, modificar y estructurar el esquema** de una base de datos. En otras palabras, se encarga de construir y organizar "el contenedor" (tablas, columnas, índices, restricciones) donde posteriormente se guardará la información, sin manipular directamente los datos que contienen.

### Principales comandos DDL
Las operaciones más comunes que pertenecen a este grupo son:

* **`CREATE`**: Se utiliza para crear nuevos objetos en la base de datos (como una base de datos completa, una tabla, una vista o un índice).
* **`ALTER`**: Permite modificar la estructura de un objeto ya existente (por ejemplo, añadir una columna nueva a una tabla, cambiar el tipo de dato de un campo o renombrarlo).
* **`DROP`**: Elimina por completo un objeto de la base de datos (como una tabla entera con todos sus datos y su estructura).
* **`TRUNCATE`**: Vacía rápidamente una tabla, borrando todos sus registros, pero manteniendo intacta su estructura para volver a usarla.
* **`RENAME`**: Sirve para cambiarle el nombre a un objeto existente.

### Ejemplo práctico de DDL
Una sentencia DDL para definir y crear una tabla de usuarios desde cero sería:

```sql
CREATE TABLE usuarios (
    id INT PRIMARY KEY,
    nombre VARCHAR(50),
    correo VARCHAR(100)
);
```