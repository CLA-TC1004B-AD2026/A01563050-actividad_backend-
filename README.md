# Actividad: Servicios Web usando MSSQLServer como base de datos
Este repositorio contiene una actividad de conexión a una instancia de **SQL Server** que corre dentro de un contenedor Docker en **GitHub Codespaces** utilizando el paquete **pymssql** para Python.

## Prerequisitos

Antes de comenzar, asegúrate de tener:

- **GitHub Codespaces** habilitado.
- **Docker** ejecutándose en tu Codespace.
- **Python 3** instalado.
- **pymssql** instalado en tu entorno Python.

### Iniciar la instancia de SQL Server en Docker

Para iniciar una instancia de **SQL Server** en un contenedor Docker, ejecuta el siguiente comando en la terminal de tu **GitHub Codespace**:

```sh
docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=YourPassword123!' \
   -p 1433:1433 --name sqlserver -d mcr.microsoft.com/mssql/server:2022-latest
```

### Instalar sqlcmd (IMPORTANTE: copiar linea por linea)
```sh
curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt update
sudo apt install mssql-tools unixodbc-dev
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc
```

 Usar sqlcmd para conectarse desde la terminal
```sh
sqlcmd -S localhost -U sa -P YourPassword123! -C
```
***

## ACTIVIDAD
### 1. GENERA una tabla de películas con al menos los siguientes campos: nombre_pelicula, clasificacion_pelicula

Recuerda tener una campo ID que sea AUTOINCREMENTAL


### 2. Agrega al menos 3 peliculas

Usa la sentencia INSERT para agregar al menos 3 peliculas

### Cerrar sqlcmd
```sh
quit
```

### 3. Genera un programa en python que implemente los servicios web C (create) y R (read) para la tabla películas

Puedes editar el programa ws.py del ejercicio previo

#### Prerequisitos

- Se ejecutaron los comandos SQL previos


#### Ejecución de servidor de servicios web

Una vez modificado el archivo, puedes ejecutar el siguiente comando en la terminal de tu **GitHub Codespace**:

```sh
cd web\ services/
python ws.py

```
### 4. Genera ejemplos para consumir servicios web desde la terminal

Abra **otra terminal**  (no cierre la terminal que está ejecutando el servidor) para probar sus servicios web.

#### A. **CREATE (Crear una película)**

Utilizamos el método `POST` y enviamos los datos en formato JSON.

#### B. **READ (Leer todas las películas)**

Utilizamos el método `GET` para obtener la lista completa.

### 5. Prueba tus servicios web desde Postman

Prueba AMBOS servicios web desde Postman. Recuerda que después de correr tus servicios web, deberás cambiar la visibilidad a pública para poderlo probar desde tu computadora usando Yaak o Postman.

### ¿Qué entregarás?

Un PDF con dos screenshots, 1 haciendo POST desde postman, otro haciendo GET desde postman, donde se muestre que hay más de 3 registros (dado que al menos insertaste otro con POST).


