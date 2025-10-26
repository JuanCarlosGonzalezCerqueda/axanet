# Actividad II - Sistema de Gestión de Clientes Axanet

## Introducción

¡Estimados estudiantes!

Bienvenidos a la **Actividad II**. En la actividad anterior, diseñaron conceptualmente una solución para la empresa Axanet. Ahora, llevarán esas ideas a la práctica desarrollando una aplicación en Python para gestionar la información de los clientes de Axanet. Además, utilizarán **GitHub** para alojar su proyecto, simular trabajo colaborativo y automatizar ciertas notificaciones mediante **GitHub Actions**.

## Recordatorio del Problema de Axanet

Axanet necesita una aplicación que permita:

- **Crear un archivo para un nuevo cliente**: Guardar su información y la descripción del primer servicio
- **Consultar información de un cliente existente**: Ya sea buscando por nombre o listando todos
- **Modificar información de un cliente existente**: Específicamente, agregar una nueva solicitud de servicio a su archivo
- **Eliminar la información de un cliente**

## ¿Qué se espera que hagan en ESTA ACTIVIDAD PRÁCTICA?

El entregable principal constará de:

1. **Un programa en Python**
2. **Un proyecto en GitHub con flujos de GitHub Actions**
3. **Un video demostrativo**
4. **Un documento Word con explicaciones y diagramas**

---

## Parte 1: Programa en Python

Este es el núcleo de la actividad. Desarrollarán una aplicación de consola en Python.

### Objetivo
Crear un programa en Python que permita agregar, modificar, eliminar y visualizar la información de los clientes de Axanet, almacenada en archivos de texto individuales.

### Funcionalidades Requeridas del Programa Python

#### Gestión de Archivos de Clientes
- El programa debe operar sobre un directorio específico donde se guardan los archivos de los clientes (ej. `axanet_clientes_python/`)
- Cada cliente tendrá su propio archivo de texto (ej. `juan_perez.txt`)

#### Crear Nuevo Cliente
- Solicitar el nombre del nuevo cliente y la descripción del primer servicio
- Crear un archivo de texto con información normalizada: **Nombre**, **ID_Cliente**, **Teléfono**, **Correo**, **FechaRegistro** y el primer servicio con su fecha

#### Visualizar Información de Cliente
- Permitir ingresar el nombre de un cliente y mostrar su archivo
- O listar todos los archivos de clientes existentes

#### Modificar Cliente Existente (Agregar Servicio)
- Permitir seleccionar un cliente y agregar un nuevo servicio al final de su archivo

#### Eliminar Información de Cliente
- Seleccionar un cliente y eliminar su archivo con confirmación

#### Uso de Tablas Hash (Diccionarios en Python)
- Asociar nombre del cliente con su archivo usando diccionarios
- Cargar información temporalmente al leer un archivo para facilitar la manipulación

### Sugerencia de estructura de archivo:

```
Nombre: Ana Garcia
ID_Cliente: AG_20240519153045
Telefono: 5512345678
Correo: ana.garcia@email.com
FechaRegistro: 2024-05-19
Servicios:
- Solicitud de manufactura de pieza X (2024-05-19)
- Solicitud de diseño de prototipo Y (2024-05-20)
```

### Buenas Prácticas en Python
- **Modularización con funciones**
- **Comentarios explicativos**
- **Manejo básico de errores**
- **Buenas convenciones de nombres**

---

## Parte 2: Proyecto en GitHub y GitHub Actions

Aquí integran su desarrollo con herramientas de colaboración y automatización.

### Objetivo
Alojar el programa Python en un repositorio de GitHub, simular la colaboración con otros usuarios y configurar **GitHub Actions** para automatizar notificaciones.

### ¿Qué hacer?

#### Crear un Proyecto (Repositorio) en GitHub
- Crear un nuevo repositorio en su cuenta de GitHub
- Incluir `README.md` con descripción del proyecto y cómo ejecutarlo
- Incluir `.gitignore` para ignorar archivos innecesarios (como `__pycache__/`, `.env`, etc.)

#### Simular Colaboración (Mínimo 2 usuarios ficticios + ustedes)
- Añadir dos cuentas de GitHub como colaboradores
- Simular al menos un commit de otro usuario (modificación simple al README o comentario al código)

#### Alojar la Aplicación en GitHub
- Subir el código Python y organizarlo adecuadamente

#### Generar Flujos en GitHub Actions (Mínimo Tres)

**Objetivo de los Flujos**: Simular una notificación al equipo mediante un echo en el log cuando se crea, actualiza o consulta un cliente.

**Desencadenadores**:
- Cada flujo se activa manualmente desde GitHub UI (usando `workflow_dispatch`)

##### Flujo 1: Creación de un Nuevo Cliente
```yaml
name: New Client Notification
on:
  workflow_dispatch:
jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Notify Team
        run: echo "NEW CLIENT CREATED: [Nombre]. Notifying team: [UsuarioGitHub], Colaborador1, Colaborador2."
```

##### Flujo 2: Actualización de Cliente
```yaml
name: Client Update Notification
on:
  workflow_dispatch:
jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Notify Team
        run: echo "CLIENT UPDATED: [Nombre]. Notifying team: ..."
```

##### Flujo 3: Consulta de Cliente
```yaml
name: Client Query Notification
on:
  workflow_dispatch:
jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Notify Team
        run: echo "CLIENT QUERY: [Nombre]. Notifying team: ..."
```

### ¿Cómo hacerlo?

1. Crear archivos `.github/workflows/` con los workflows YAML
2. Ejecutarlos desde la pestaña **Actions** > **Run workflow** en GitHub
3. **Incluir en el Documento Word**: Capturas de ejecución del workflow y el log del mensaje de notificación

---

## Parte 3: Video Demostrativo

### Objetivo
Mostrar la aplicación funcionando y los flujos de GitHub Actions.

### Contenido del Video

#### Aplicación Python
- Ejecutar el programa
- Mostrar las 5 funcionalidades:
  1. Crear cliente
  2. Visualizar cliente
  3. Actualizar cliente
  4. Eliminar cliente
  5. Listar todos los clientes

#### GitHub Actions
- Ir a GitHub > **Actions**
- Ejecutar manualmente los workflows
- Mostrar los logs con los mensajes de notificación

### Calidad del Video
- **Video y audio claros**
- **Ritmo adecuado**
- **Enfoque profesional**

---

## Parte 4: Documento en Word

### Objetivo
Explicar todo lo realizado.

### Contenido

1. **Portada**
2. **Introducción**
3. **Diagrama de Flujo** de la aplicación Python
4. **Pseudocódigo** de funciones principales
5. **Explicación del código** y uso de diccionarios
6. **Capturas del proyecto en GitHub** y colaboración
7. **Descripción de los flujos GitHub Actions**
8. **Liga al repositorio**
9. **Capturas de ejecución**

---

## Consejos Finales

1. **Empiecen por Python** - Es la base de todo
2. **Configuren GitHub temprano** - No lo dejen para el final
3. **Prueben los workflows antes de grabar** - Asegúrense de que funcionan
4. **Documenten después de validar** que todo funcione
5. **Practiquen el video** antes de la grabación final

---

## ¡Mucho éxito!

Esta actividad les ayudará a conectar el desarrollo de software con las mejores prácticas de trabajo colaborativo y automatización usando las herramientas más populares del ecosistema de desarrollo moderno.

---

### Repositorio de Referencia
```
https://github.com/usuario/axanet-client-manager
```

> **Nota**: Cambien la URL por la de su repositorio actual una vez creado en GitHub.