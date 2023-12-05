import os
import subprocess
import time
import signal
import sys

def ejecutar_proceso(nombre_proceso, comando):
    try:
        proceso = subprocess.Popen(comando, shell=True, preexec_fn=os.setsid)
        print(f"Proceso {nombre_proceso} iniciado con PID: {proceso.pid}")
        return proceso

    except Exception as e:
        print(f"Error al iniciar el proceso {nombre_proceso}: {e}")
        sys.exit(1)

def monitorear_proceso(proceso, nombre_proceso, comando):
    while True:
        estado = proceso.poll()

        if estado is not None:
            print(f"El proceso {nombre_proceso} se ha cerrado con estado: {estado}. Reiniciando...")
            proceso = ejecutar_proceso(nombre_proceso, comando)

        time.sleep(5)  # Espera 5 segundos antes de verificar nuevamente

def main():
    if len(sys.argv) != 3:
        print("Uso: python script.py <nombre_proceso> <comando_a_ejecutar>")
        sys.exit(1)

    nombre_proceso = sys.argv[1]
    comando = sys.argv[2]

    proceso = ejecutar_proceso(nombre_proceso, comando)
    monitorear_proceso(proceso, nombre_proceso, comando)

if __name__ == "__main__":
    main()
