# ToDo List API
## Funcionalidades
**Registro de usuarios:** Esta API permite crear usuarios a partir del nombre, email y contraseña

**Inicio de sesion:** Los usuarios registrados pueden autenticarse para recibir un token que necesitaran para hacer solicitudes

**Operaciones:** La API permite ver,crear,actualizar y borrar tareas

## Instalacion de la api

### 1 Clona el repositorio
```
git clone https://github.com/Exeperdom0/todo-api
```

### 2 Instala las dependencias
```
pip install -r requeriments.txt
```
## Endpoints
  
  ### **Registro:**

  **URL:** /register
  
  **Metodo:** Post

**Asi se ve una solicitud:**
```
  {
    "name":"name",
    "email":"email",
    "password":"password"
  }
```

  ### **Autenticacion:**

  **URL:** /login

  **Metodos:** Post

**Asi se ve una solicitud:**
```
  {
    "email":"email",
    "password":"password"
  }
```
  ### **Creacion de tarea:**

  **URL:**/todos
  
  **Metodos:** Post

**Asi se ve una solicitud**
```
  {
    "title":"titulo de la tarea",
    "description":"detalles de la tarea"
  }
```
  
  ### **Actualizacion:**

  **URL:**/todos/<id_de_la_tarea>

  **Metodos:** Put

  **Asi se ve una solicitud:**
```
  {
    "title":"titulo de la tarea",
    "description":"detalles de la tarea"
  }
```

  ### **Eliminacion:**

  **URL:**/todos/<id_de_la_tarea>

  **Metodos:** Delete

  ### **Ver tareas:**

  **URL:**/todos/<numero_de_pagina>/<limite_de_tareas_para_ver> 

  **Metodos:** Get

**Cualquier sugerencia es mas que bienvenida**

https://roadmap.sh/projects/todo-list-api
