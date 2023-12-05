# Randy Cascante Espinoza C11718


# Script 1: Monitoreo de Información de Procesos
python
Copy code
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
# Explicación:

Este script utiliza el módulo psutil para obtener información sobre un proceso dado su ID.
Toma el ID del proceso como argumento de línea de comandos.
Muestra información como el nombre, ID, ID del proceso padre, usuario propietario, porcentaje de uso de CPU, consumo de memoria, estado y ruta del ejecutable.
Se ejecuta desde la línea de comandos: python script.py <ID_del_proceso>.

# Script 2: Monitoreo y Reinicio Automático de Proceso
python
Copy code
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
    
# Explicación:

Este script ejecuta un proceso con un nombre y comando dados.
Monitorea continuamente el estado del proceso y lo reinicia automáticamente si se cierra.
Toma el nombre del proceso y el comando como argumentos de línea de comandos.
Se ejecuta desde la línea de comandos: python script.py <nombre_proceso> <comando_a_ejecutar>.

# Script 3: Monitoreo y Graficación del Consumo de CPU y Memoria
python
Copy code
import os
import psutil
import subprocess
import time
import matplotlib.pyplot as plt
from datetime import datetime

def ejecutar_proceso(ejecutable):
    try:
        proceso = subprocess.Popen(ejecutable, shell=True, preexec_fn=os.setsid)
        print(f"Proceso iniciado con PID: {proceso.pid}")
        return proceso
    except Exception as e:
        print(f"Error al iniciar el proceso: {e}")
        return None

def monitorear_proceso(proceso, intervalo, log_file):
    tiempos = []
    cpu_uso = []
    memoria_uso = []

    try:
        while True:
            tiempo_actual = datetime.now()
            tiempos.append(tiempo_actual)

            uso_cpu = proceso.cpu_percent()
            uso_memoria = proceso.memory_info().rss

            cpu_uso.append(uso_cpu)
            memoria_uso.append(uso_memoria)

            with open(log_file, 'a') as log:
                log.write(f"{tiempo_actual} - CPU: {uso_cpu}% | Memoria: {uso_memoria} bytes\n")

            time.sleep(intervalo)
    except KeyboardInterrupt:
        # Detener el monitoreo si se presiona Ctrl+C
        pass

    return tiempos, cpu_uso, memoria_uso

def graficar_resultados(tiempos, cpu_uso, memoria_uso):
    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    plt.plot(tiempos, cpu_uso, label='CPU Usage', color='blue')
    plt.title('Consumo de CPU a lo largo del tiempo')
    plt.xlabel('Tiempo')
    plt.ylabel('Porcentaje de uso')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(tiempos, memoria_uso, label='Memory Usage', color='green')
    plt.title('Consumo de Memoria a lo largo del tiempo')
    plt.xlabel('Tiempo')
    plt.ylabel('Uso de memoria (bytes)')
    plt.legend()

    plt.tight_layout()
    plt.show()

def main():
    if len(os.sys.argv) != 2:
        print("Uso: python script.py <ejecutable>")
        os.sys.exit(1)

    ejecutable = os.sys.argv[1]
    intervalo = 1  # Intervalo de tiempo en segundos
    log_file = "log.txt"

    proceso = ejecutar_proceso(ejecutable)
    if proceso is None:
        os.sys.exit(1)

    tiempos, cpu_uso, memoria_uso = monitorear_proceso(proceso, intervalo, log_file)
    proceso.terminate()

    graficar_resultados(tiempos, cpu_uso, memoria_uso)

if __name__ == "__main__":
    main()
    
# Explicación:

Este script ejecuta un proceso especificado como argumento y monitorea su consumo de CPU y memoria.
Registra los valores en un archivo de log y, al finalizar, crea gráficos utilizando matplotlib.
Toma el ejecutable como argumento de línea de comandos.
Se ejecuta desde la línea de comandos: python script.py <ejecutable>.