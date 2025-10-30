from datetime import datetime
from typing import List
import re

from .excepciones import ErrorValidacion


class Servicio:
    def __init__(self, descripcion: str, fecha_solicitud: str):
        self.descripcion = descripcion.strip()
        if fecha_solicitud:
            self.fecha_solicitud = fecha_solicitud
        else:
            ahora = datetime.now()
            self.fecha_solicitud = ahora.strftime("%Y-%m-%d %H:%M:%S")
    
    def __str__(self):
        return f"{self.descripcion} ({self.fecha_solicitud})"

class Cliente:
    def __init__(self, nombre: str, telefono: str, email: str):
        self.nombre = nombre.strip()
        self.telefono = telefono.strip()
        self.email = email.strip()
        self.servicios: List[Servicio] = []
        self.id_cliente = ""
        ahora = datetime.now()
        self.fecha_registro = ahora.strftime("%Y-%m-%d")
        self.validar_datos()
    
    @property
    def nombre_normalizado(self) -> str:
        normalizado = self.nombre.lower()
        reemplazos = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'ñ': 'n', 'ç': 'c', ' ': '_'
        }
        for original, reemplazo in reemplazos.items():
            normalizado = normalizado.replace(original, reemplazo)
        normalizado = re.sub(r'[^a-z0-9_]', '', normalizado)
        return normalizado
    
    def validar_datos(self):
        if not self.nombre or len(self.nombre.strip()) < 2:
            raise ErrorValidacion(
                campo="nombre",
                valor=self.nombre,
                motivo="Nombre no valido"
            )
        telefono_limpio = re.sub(r'[^\d]', '', self.telefono)
        if len(telefono_limpio) != 10:
            raise ErrorValidacion(
                campo="telefono",
                valor=self.telefono,
                motivo="Telefono no es correcto"
            )
        self.telefono = telefono_limpio
        patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron_email, self.email):
            raise ErrorValidacion(
                campo="email",
                valor=self.email,
                motivo="Correo no valido"
            )

    def generar_id_cliente(self) -> str:
        palabras = self.nombre.split()
        iniciales = ""   
        for palabra in palabras[:2]:
            if palabra:
                iniciales += palabra[0].upper()
        if len(iniciales) < 2:
            iniciales = (iniciales + self.nombre[:2].upper())[:2]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        id_cliente = f"{iniciales}_{timestamp}"
        return id_cliente
    
    def agregar_servicio(self, descripcion: str):
        if not descripcion or not descripcion.strip():
            raise ErrorValidacion(
                campo="descripcion_servicio",
                valor=descripcion,
                motivo="La descripción del servicio no puede estar vacía"
            )
        nuevo_servicio = Servicio(descripcion, None)
        self.servicios.append(nuevo_servicio)
    
    def a_formato_archivo(self) -> str:
        contenido = []
        contenido.append(f"Nombre: {self.nombre}")
        contenido.append(f"ID_Cliente: {self.id_cliente}")
        contenido.append(f"Telefono: {self.telefono}")
        contenido.append(f"Correo: {self.email}")
        contenido.append(f"FechaRegistro: {self.fecha_registro}")
        contenido.append("Servicios:")
        for servicio in self.servicios:
            contenido.append(f"- {servicio.descripcion} ({servicio.fecha_solicitud})")
        return "\n".join(contenido)
    
    @classmethod
    def desde_archivo(cls, contenido_archivo: str) -> 'Cliente':
        lineas = contenido_archivo.strip().split('\n')
        nombre = ""
        telefono = ""
        email = ""
        id_cliente = ""
        fecha_registro = ""
        servicios_seccion = False
        servicios_encontrados = []
        for linea in lineas:
            linea = linea.strip()
            if linea.startswith("Nombre:"):
                nombre = linea.split(":", 1)[1].strip()
            elif linea.startswith("ID_Cliente:"):
                id_cliente = linea.split(":", 1)[1].strip()
            elif linea.startswith("Telefono:"):
                telefono = linea.split(":", 1)[1].strip()
            elif linea.startswith("Correo:"):
                email = linea.split(":", 1)[1].strip()
            elif linea.startswith("FechaRegistro:"):
                fecha_registro = linea.split(":", 1)[1].strip()
            elif linea == "Servicios:":
                servicios_seccion = True
            elif servicios_seccion and linea.startswith("- "):
                servicio_texto = linea[2:]
                if "(" in servicio_texto and ")" in servicio_texto:
                    partes = servicio_texto.rsplit("(", 1)
                    if len(partes) == 2:
                        descripcion = partes[0].strip()
                        fecha_parte = partes[1].rstrip(")")
                        servicios_encontrados.append((descripcion, fecha_parte))
                    else:
                        servicios_encontrados.append((servicio_texto, None))
                else:
                    servicios_encontrados.append((servicio_texto, None))
        cliente = cls(nombre=nombre, telefono=telefono, email=email)
        cliente.id_cliente = id_cliente
        cliente.fecha_registro = fecha_registro
        for descripcion, fecha in servicios_encontrados:
            servicio = Servicio(descripcion, fecha)
            cliente.servicios.append(servicio)
        return cliente
    
    def __str__(self):
        return f"{self.nombre} (ID: {self.id_cliente}, Servicios: {len(self.servicios)})"
    
    def __repr__(self):
        return f"Cliente(nombre='{self.nombre}', telefono='{self.telefono}', email='{self.email}')"