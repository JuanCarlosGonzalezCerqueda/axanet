class ClienteError(Exception):
    def __init__(self, mensaje: str, nombre_cliente: str):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.nombre_cliente = nombre_cliente

class ClienteNoEncontradoError(ClienteError):
    def __init__(self, nombre_cliente: str):
        mensaje = f"No se encontró un cliente con el nombre '{nombre_cliente}'"
        super().__init__(mensaje, nombre_cliente)

class ClienteExisteError(ClienteError):
    def __init__(self, nombre_cliente: str):
        mensaje = f"Ya existe un cliente con el nombre '{nombre_cliente}'"
        super().__init__(mensaje, nombre_cliente)

class ErrorValidacion(ClienteError):
    def __init__(self, campo: str, motivo: str):
        self.campo = campo
        self.motivo = motivo
        super().__init__(f"Error de validación en {campo}: {motivo}")

class ErrorArchivo(ClienteError):
    def __init__(self, operacion: str, nombre_archivo: str, motivo: str):
        mensaje = f"Error al {operacion} el archivo '{nombre_archivo}': {motivo}"
        super().__init__(mensaje)
        self.operacion = operacion
        self.nombre_archivo = nombre_archivo
        self.motivo = motivo