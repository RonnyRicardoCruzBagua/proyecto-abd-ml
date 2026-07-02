# Configuración del Rol Administrador

## Introducción

La administración de roles y permisos es una práctica fundamental para garantizar la seguridad y el control de acceso dentro de una base de datos. Mediante la asignación adecuada de privilegios es posible gestionar el acceso a los distintos recursos del sistema, asegurando que cada usuario disponga únicamente de las autorizaciones necesarias para realizar sus funciones.

En esta actividad se implementó un rol administrativo dentro de la base de datos **HotelDB**, utilizada en el proyecto **Hotel Booking Demand**. El rol fue configurado para administrar el acceso a las principales tablas y objetos de la base de datos, permitiendo realizar operaciones de consulta y gestión de información.

---

# Objetivo General

Implementar y configurar un rol administrador en la base de datos HotelDB que permita gestionar el acceso a los objetos principales del sistema mediante la asignación de privilegios adecuados.

---

# Objetivos Específicos

- Crear un rol administrativo dentro de la base de datos.
- Crear y asociar un usuario al rol administrador.
- Configurar permisos mediante sentencias GRANT.
- Administrar privilegios mediante sentencias REVOKE.
- Verificar el acceso a tablas y vistas de la base de datos.
- Realizar pruebas de privilegios para validar la configuración implementada.

---

# Descripción de la Actividad

La actividad consistió en la implementación de un rol denominado **RolAdministrador**, encargado de centralizar los privilegios administrativos dentro de la base de datos.

Se creó un usuario de prueba asociado al rol para verificar el funcionamiento de los permisos asignados. Posteriormente se configuraron privilegios sobre las tablas principales del sistema utilizando sentencias **GRANT**, permitiendo operaciones de consulta, inserción, actualización y eliminación de registros.

Además, se aplicaron instrucciones **REVOKE** con el fin de demostrar la capacidad de administrar y retirar permisos específicos cuando sea necesario.

Finalmente, se realizaron pruebas de acceso utilizando el usuario asociado al rol para validar la correcta configuración de privilegios sobre los diferentes objetos de la base de datos.

---

# Base de Datos Utilizada

**HotelDB**

---

# Estructura de Archivos

## 1. Crear rol administrador.sql

Script encargado de crear el rol **RolAdministrador** en la base de datos.

Funciones principales:

- Verificar la existencia del rol.
- Crear el rol cuando no exista.
- Evitar duplicidades dentro de la base de datos.

---

## 2. Usuario administrador.sql

Script utilizado para crear un usuario de prueba y asociarlo al rol administrador.

Funciones principales:

- Crear el usuario.
- Agregar el usuario al RolAdministrador.
- Validar la asignación del rol.

---

## 3. Asignar permisos administrador.sql

Script encargado de configurar los privilegios del rol mediante sentencias SQL.

Permisos implementados:

- SELECT
- INSERT
- UPDATE
- DELETE

Además, se incluyeron sentencias REVOKE para la administración de privilegios específicos.

---

## 4. Pruebas de acceso.sql

Script utilizado para validar el funcionamiento del rol y verificar el acceso a los objetos de la base de datos.

Las pruebas realizadas permitieron comprobar:

- Acceso a tablas.
- Acceso a vistas.
- Correcta asignación de permisos.
- Funcionamiento del usuario asociado al rol.

---

# Objetos Utilizados

Durante la implementación y validación del rol se trabajó con los siguientes objetos:

## Tablas

- dbo.Clientes
- dbo.Reservas
- dbo.Hoteles
- dbo.Habitaciones
- dbo.CanalesReserva
- dbo.EstadosReserva
- dbo.FechasLlegada

### Descripción

**Clientes:** almacena la información de los clientes registrados.

**Reservas:** contiene la información relacionada con las reservas hoteleras.

**Hoteles:** almacena la información general de los hoteles registrados en el sistema.

**Habitaciones:** contiene los datos relacionados con las habitaciones disponibles y asignadas en las reservas.

**CanalesReserva:** registra los distintos canales utilizados para realizar las reservas.

**EstadosReserva:** almacena los estados asociados a las reservas.

**FechasLlegada:** contiene información relacionada con las fechas de llegada de los huéspedes.

---

## Vista Utilizada

### dbo.vw_resumen_reservas

Vista utilizada para validar el acceso del RolAdministrador a objetos distintos de las tablas base.

La consulta realizada sobre esta vista permitió comprobar que el usuario asociado al rol puede acceder correctamente a información derivada de las tablas de la base de datos, verificando así los privilegios otorgados.

---

# Implementación de Seguridad

La administración de permisos se realizó mediante la utilización de roles, permitiendo centralizar los privilegios asignados a los usuarios.

Entre los beneficios obtenidos se encuentran:

- Organización de permisos.
- Facilidad en la administración de usuarios.
- Mayor control sobre los accesos.
- Reducción de configuraciones redundantes.
- Aplicación de buenas prácticas de seguridad en SQL Server.

---

# Validación

La validación se realizó mediante las siguientes etapas:

1. Creación del RolAdministrador.
2. Creación del usuario asociado al rol.
3. Asignación de privilegios mediante GRANT.
4. Administración de permisos mediante REVOKE.
5. Ejecución de consultas sobre tablas del sistema.
6. Verificación de acceso a la vista `vw_resumen_reservas`.
7. Confirmación del correcto funcionamiento de los privilegios asignados.

Todas las pruebas fueron ejecutadas satisfactoriamente, permitiendo comprobar que el usuario asociado al rol dispone de los permisos necesarios para acceder a los objetos autorizados.

---

# Resultados Obtenidos

La implementación permitió crear un entorno de administración controlado dentro de la base de datos HotelDB mediante el uso de un rol dedicado para tareas administrativas.

Las pruebas realizadas sobre tablas y vistas confirmaron la correcta asignación de permisos y el adecuado funcionamiento del modelo de seguridad implementado.

---

# Conclusiones

La implementación del **RolAdministrador** permitió centralizar la gestión de privilegios dentro de la base de datos, facilitando la administración de usuarios y el control de acceso a los recursos del sistema.

El uso de sentencias **GRANT** y **REVOKE** permitió gestionar adecuadamente los privilegios asignados y validar el funcionamiento de los mecanismos de seguridad proporcionados por SQL Server.

La actividad cumplió satisfactoriamente con los objetivos planteados, verificando el acceso a tablas y vistas mediante pruebas de privilegios ejecutadas con un usuario asociado al rol administrador.