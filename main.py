#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Agregar la carpeta src al path de Python para importar nuestros módulos
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Importar nuestros módulos personalizados
from axanet.cliente_manager import ClienteManager
from axanet.excepciones import (
    ClienteNoEncontradoError, 
    ClienteExisteError,
    ErrorValidacion
)


class AplicacionAxanet:
    def __init__(self):

        
        self.gestor_clientes = ClienteManager()

    def mostrar_menu(self):
        os.system('cls')
        """Muestra las opciones disponibles en el menú principal."""
        print("\nMENÚ PRINCIPAL")
        print("─" * 35)
        print("1. Crear nuevo cliente")
        print("2. Buscar cliente por nombre") 
        print("3. Ver todos los clientes")
        print("4. Agregar servicio a cliente")
        print("5. Eliminar cliente")
        print("0. Salir")
        print("─" * 35)

    def crear_cliente(self):
        print("\nCREAR NUEVO CLIENTE")
        print("─" * 25)
        
        try:
            nombre = input("Nombre completo del cliente: ").strip()
            if not nombre:
                print("Campo obligatorio")
                return
                
            telefono = input("Teléfono (10 dígitos): ").strip()
            if not telefono:
                print("Campo obligatorio")
                return
                
            email = input("Correo electrónico: ").strip()
            if not email:
                print("Campo obligatorio")
                return
                
            primer_servicio = input("Descripción del primer servicio: ").strip()
            if not primer_servicio:
                print("Campo obligatorio")
                return

            cliente = self.gestor_clientes.crear_cliente(
                nombre=nombre,
                telefono=telefono, 
                email=email,
                primer_servicio=primer_servicio
            )
            
            print(f"Cliente creado exitosamente!")
            input("Presiona Enter para continuar...")
            os.system('cls')
            
        except ClienteExisteError as e:
            print(f"Cliente ya esta en la base")
            input("Presiona Enter para continuar...")
            os.system('cls')
        except ErrorValidacion as e:
            print(f"❌ Error de validación: {e}")
            input("Presiona Enter para continuar...")
            os.system('cls')
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            input("Presiona Enter para continuar...")
            os.system('cls')

    def buscar_cliente(self):
        print("\nBUSCAR CLIENTE")
        print("─" * 17)
        
        nombre = input("Ingrese el nombre del cliente: ").strip()
        if not nombre:
            print("campo obligatorio")
            return
            
        try:
            cliente = self.gestor_clientes.obtener_cliente(nombre)
            print("Cliente encontrado:")
            print(f"Nombre: {cliente.nombre}")
            print(f"ID: {cliente.id_cliente}")
            print(f"Teléfono: {cliente.telefono}")
            print(f"Email: {cliente.email}")
            print(f"Registrado: {cliente.fecha_registro}")
            print(f"\nSERVICIOS ({len(cliente.servicios)}):")
            
            for i, servicio in enumerate(cliente.servicios, 1):
                print(f"   {i}. {servicio.descripcion}")
                print(f"      Fecha: {servicio.fecha_solicitud}")
            input("Presiona Enter para continuar...")
            os.system('cls')
                
        except ClienteNoEncontradoError:
            print(f"No se encontró un cliente con el nombre '{nombre}'")
            input("Presiona Enter para continuar...")
            os.system('cls')
        except Exception as e:
            print(f"Error al buscar: {e}")
            input("Presiona Enter para continuar...")
            os.system('cls')

    def listar_todos_clientes(self):
        print("\nTODOS LOS CLIENTES")
        print("─" * 21)
        
        try:
            clientes = self.gestor_clientes.listar_todos_clientes()
            
            if not clientes:
                print("No hay clientes registrados en el sistema")
                input("Presiona Enter para continuar...")
                os.system('cls')
                return
            
            print(f"Se encontraron {len(clientes)} cliente(s):\n")
            
            for i, cliente in enumerate(clientes, 1):
                nombre_corto = cliente.nombre[:22] + "..." if len(cliente.nombre) > 25 else cliente.nombre
                print(f"{i:<3} {nombre_corto:<25} {cliente.telefono:<12} {len(cliente.servicios):<10}")
                
            print("─" * 55)
            print(f"Total: {len(clientes)} cliente(s)")
            input("Presiona Enter para continuar...")
            os.system('cls')
            
        except Exception as e:
            print(f"Error al listar clientes: {e}")
            input("Presiona Enter para continuar...")
            os.system('cls')

    def agregar_servicio(self):
        print("\nAGREGAR SERVICIO A CLIENTE")
        print("─" * 29)
        
        nombre = input("Nombre del cliente: ").strip()
        if not nombre:
            print("Campo obligatorio")
            return
        try:
            cliente = self.gestor_clientes.obtener_cliente(nombre)
            print(f"Cliente encontrado: {cliente.nombre}")
            print(f"Servicios actuales: {len(cliente.servicios)}")
            nuevo_servicio = input("Descripción del nuevo servicio: ").strip()
            if not nuevo_servicio:
                print("Campo obligatorio")
                return
                
            print("Agregando servicio...")
            cliente_actualizado = self.gestor_clientes.agregar_servicio_cliente(
                nombre, nuevo_servicio
            )
            
            print("Servicio agregado exitosamente!")
            print(f"Total de servicios: {len(cliente_actualizado.servicios)}")
            input("Presiona Enter para continuar...")
            os.system('cls')
            
            
        except ClienteNoEncontradoError:
            print(f"No se encontró un cliente con el nombre '{nombre}'")
            input("Presiona Enter para continuar...")
            os.system('cls')
        except Exception as e:
            print(f"Error al agregar servicio: {e}")
            input("Presiona Enter para continuar...")
            os.system('cls')

    def eliminar_cliente(self):
        print("\nELIMINAR CLIENTE")
        print("─" * 18)
        nombre = input("Nombre del cliente a eliminar: ").strip()
        if not nombre:
            print("Campo obligatorio")
            return
            
        try:
            cliente = self.gestor_clientes.obtener_cliente(nombre)
            print(f"\n  ATENCIÓN: Se eliminará el siguiente cliente:")
            print(f" Nombre: {cliente.nombre}")
            print(f" Teléfono: {cliente.telefono}")
            print(f" Servicios: {len(cliente.servicios)}")
            confirmacion = input("\n¿Está seguro? (escriba 'SI' para confirmar): ").strip().upper()
            
            if confirmacion == "SI":
                print(" Eliminando cliente...")
                exito = self.gestor_clientes.eliminar_cliente(nombre)
                
                if exito:
                    print("Cliente eliminado exitosamente")
                    input("Presiona Enter para continuar...")
                    os.system('cls')
                else:
                    print("No se pudo eliminar el cliente")
                    input("Presiona Enter para continuar...")
                    os.system('cls')
            else:
                print("Operación cancelada")
                input("Presiona Enter para continuar...")
                os.system('cls')
                
        except ClienteNoEncontradoError:
            print(f" No se encontró un cliente con el nombre '{nombre}'")
            input("Presiona Enter para continuar...")
            os.system('cls')
        except Exception as e:
            print(f" Error al eliminar: {e}")
            input("Presiona Enter para continuar...")
            os.system('cls')

    def ejecutar(self):
        while True:
            try:
                self.mostrar_menu()
                opcion = input("\n Seleccione una opción (0-5): ").strip()
                
                if opcion == "0":
                    os.system('cls')
                    break
                elif opcion == "1":
                    os.system('cls')
                    self.crear_cliente()
                elif opcion == "2":
                    os.system('cls')
                    self.buscar_cliente()
                    os.system('cls')
                elif opcion == "3":
                    os.system('cls')
                    self.listar_todos_clientes()
                elif opcion == "4":
                    os.system('cls')
                    self.agregar_servicio()
                elif opcion == "5":
                    os.system('cls')
                    self.eliminar_cliente()
                else:
                    print("Seleccion invalida, intente de nuevo")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Programa interrumpido por el usuario")
                break
            except Exception as e:
                print(f"\n Error inesperado: {e}")
                print("💡 Intente nuevamente o contacte al soporte técnico")


def main():

    try:
        aplicacion = AplicacionAxanet()
        aplicacion.ejecutar()
        
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido")
    except Exception as e:
        sys.exit(1)


# Punto de entrada del programa
if __name__ == "__main__":
    main()