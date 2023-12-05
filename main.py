import os
import psutil
import sys

def obtener_informacion_proceso(pid):
    try:
        proceso = psutil.Process(pid)

        nombre_proceso = proceso.name()
        id_proceso = proceso.pid
        id_proceso_padre = proceso.ppid()
        usuario_propietario = proceso.username()
        porcentaje_cpu = proceso.cpu_percent()
        consumo_memoria = proceso.memory_info().rss
        estado = proceso.status()
        path_ejecutable = proceso.exe()

        print(f"Nombre del proceso: {nombre_proceso}")
        print(f"ID del proceso: {id_proceso}")
        print(f"Parent process ID: {id_proceso_padre}")
        print(f"Usuario propietario: {usuario_propietario}")
        print(f"Porcentaje de uso de CPU: {porcentaje_cpu}%")
        print(f"Consumo de memoria: {consumo_memoria} bytes")
        print(f"Estado: {estado}")
        print(f"Path del ejecutable: {path_ejecutable}")

    except psutil.NoSuchProcess as e:
        print(f"No se encontró un proceso con el ID {pid}.")
    except Exception as e:
        print(f"Error al obtener información del proceso: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <ID_del_proceso>")
        sys.exit(1)

    pid = int(sys.argv[1])
    obtener_informacion_proceso(pid)
