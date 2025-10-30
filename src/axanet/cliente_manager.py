import os
from pathlib import Path
from typing import Dict, List, Union

from .modelos import Cliente, Servicio
from .excepciones import (
    ClienteError,
    ClienteNoEncontradoError,
    ClienteExisteError, 
    ErrorValidacion,
    ErrorArchivo
)


class ClienteManager:

    def __init__(self, directorio_datos: str = "axanet_clients_data"):

        self._cache_clientes: Dict[str, Cliente] = {}
        self.directorio_datos = Path(directorio_datos)
        self._crear_directorio_datos()
    
    def _crear_directorio_datos(self):
        try:
            self.directorio_datos.mkdir(exist_ok=True)
        except Exception as e:
            raise ErrorArchivo(
                operacion="crear directorio",
                nombre_archivo=str(self.directorio_datos),
                motivo=str(e)
            )
    
    def _obtener_ruta_archivo(self, nombre_normalizado: str) -> Path:
        nombre_archivo = f"{nombre_normalizado}.txt"
        return self.directorio_datos / nombre_archivo
    def _cargar_cliente_desde_archivo(self, nombre_normalizado: str) -> Cliente:
        ruta_archivo = self._obtener_ruta_archivo(nombre_normalizado)
        if not ruta_archivo.exists():
            nombre_original = nombre_normalizado.replace('_', ' ').title()
            raise ClienteNoEncontradoError(nombre_original)
        
        try:
            contenido = ruta_archivo.read_text(encoding='utf-8')
            cliente = Cliente.desde_archivo(contenido)
            return cliente
            
        except Exception as e:
            raise ErrorArchivo(
                operacion="leer",
                nombre_archivo=str(ruta_archivo),
                motivo=str(e)
            )
    
    def _guardar_cliente_en_archivo(self, cliente: Cliente):
        ruta_archivo = self._obtener_ruta_archivo(cliente.nombre_normalizado)
        
        try:
            contenido = cliente.a_formato_archivo()
            ruta_archivo.write_text(contenido, encoding='utf-8')
            
        except Exception as e:
            raise ErrorArchivo(
                operacion="escribir",
                nombre_archivo=str(ruta_archivo),
                motivo=str(e)
            )
    
    def _eliminar_archivo_cliente(self, nombre_normalizado: str):
        ruta_archivo = self._obtener_ruta_archivo(nombre_normalizado)
        
        try:
            if ruta_archivo.exists():
                ruta_archivo.unlink()
            
        except Exception as e:
            raise ErrorArchivo(
                operacion="eliminar",
                nombre_archivo=str(ruta_archivo),
                motivo=str(e)
            )
    
    def _cargar_todos_clientes_a_cache(self):
        if not self.directorio_datos.exists():
            return
        archivos_clientes = list(self.directorio_datos.glob("*.txt"))
        
        for archivo in archivos_clientes:
            nombre_normalizado = archivo.stem
            if nombre_normalizado not in self._cache_clientes:
                try:
                    cliente = self._cargar_cliente_desde_archivo(nombre_normalizado)
                    self._cache_clientes[nombre_normalizado] = cliente
                except Exception as e:
                    print(f"⚠️  Advertencia: No se pudo cargar {archivo}: {e}")
    
    def crear_cliente(self, nombre: str, telefono: str, email: str, primer_servicio: str) -> Cliente:
        cliente = Cliente(nombre=nombre, telefono=telefono, email=email)
        if cliente.nombre_normalizado in self._cache_clientes:
            raise ClienteExisteError(cliente.nombre)
        
        ruta_archivo = self._obtener_ruta_archivo(cliente.nombre_normalizado)
        if ruta_archivo.exists():
            raise ClienteExisteError(cliente.nombre)
        
        cliente.id_cliente = cliente.generar_id_cliente()
        
        cliente.agregar_servicio(primer_servicio)
        
        self._guardar_cliente_en_archivo(cliente)

        self._cache_clientes[cliente.nombre_normalizado] = cliente
        
        return cliente
    
    def obtener_cliente(self, nombre: str) -> Cliente:
        cliente_temp = Cliente(nombre=nombre, telefono="0000000000", email="temp@temp.com")
        nombre_normalizado = cliente_temp.nombre_normalizado
        
        if nombre_normalizado in self._cache_clientes:
            print(f"Cliente encontrado): '{nombre_normalizado}'")
            return self._cache_clientes[nombre_normalizado]
        
        try:
            cliente = self._cargar_cliente_desde_archivo(nombre_normalizado)
            self._cache_clientes[nombre_normalizado] = cliente
            return cliente
            
        except ClienteNoEncontradoError:
            raise ClienteNoEncontradoError(nombre)
    
    def listar_todos_clientes(self) -> List[Cliente]:
        self._cargar_todos_clientes_a_cache()
        clientes = list(self._cache_clientes.values())
        clientes.sort(key=lambda c: c.nombre)
        
        print(f"Clientes en tabla: {len(self._cache_clientes)}")
        
        return clientes
    
    def agregar_servicio_cliente(self, nombre: str, descripcion_servicio: str) -> Cliente:
        cliente = self.obtener_cliente(nombre)
        cliente.agregar_servicio(descripcion_servicio)
        self._guardar_cliente_en_archivo(cliente)
        self._cache_clientes[cliente.nombre_normalizado] = cliente
        return cliente
    
    def eliminar_cliente(self, nombre: str) -> bool:
        cliente = self.obtener_cliente(nombre)
        self._eliminar_archivo_cliente(cliente.nombre_normalizado)
        if cliente.nombre_normalizado in self._cache_clientes:
            del self._cache_clientes[cliente.nombre_normalizado]
        return True
    
    def obtener_estadisticas(self) -> Dict[str, Union[int, float]]:
        self._cargar_todos_clientes_a_cache()
        total_clientes = len(self._cache_clientes)
        if total_clientes == 0:
            return {
                "total_clientes": 0,
                "total_servicios": 0,
                "promedio_servicios": 0.0
            }
        total_servicios = sum(len(cliente.servicios) for cliente in self._cache_clientes.values())
        promedio_servicios = total_servicios / total_clientes if total_clientes > 0 else 0
        return {
            "total_clientes": total_clientes,
            "total_servicios": total_servicios,
            "promedio_servicios": promedio_servicios
        }
    
    def __str__(self):
        return f"ClienteManager(clientes_en_cache={len(self._cache_clientes)})"
    
    def __repr__(self):
        return f"ClienteManager(cache_size={len(self._cache_clientes)}, directorio='{self.directorio_datos}')"

def normalizar_nombre(nombre: str) -> str:
    import re
    try:
        cliente_temp = Cliente(nombre=nombre, telefono="0000000000", email="temp@temp.com")
        return cliente_temp.nombre_normalizado
    except ErrorValidacion:
        normalizado = nombre.lower().strip()
        normalizado = normalizado.replace(' ', '_')
        normalizado = re.sub(r'[^a-z0-9_]', '', normalizado)
        return normalizado