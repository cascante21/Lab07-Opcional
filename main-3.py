
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
