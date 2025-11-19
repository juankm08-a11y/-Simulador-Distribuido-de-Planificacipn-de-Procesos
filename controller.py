import socket
import json
import time
from itertools import cycle

WORKERS = ["20.151.84.187", "20.151.61.138"]  
PORT = 9001
PROCESSES_FILE = "processes.txt"
RESULTS_FILE = "results.json"

def load_processes():
    processes = []
    with open(PROCESSES_FILE) as f:
        for line in f:
            if line.strip():
                pid, burst, prio = map(int, line.strip().split(','))
                processes.append({"process_id": pid, "burst_time": burst, "priority": prio})
    return processes

def send_to_worker(worker_ip, process):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        try:
            s.connect((worker_ip, PORT))
            s.sendall(json.dumps(process).encode())
            response = s.recv(1024)
            return json.loads(response.decode())
        except Exception as e:
            print(f"Error con {worker_ip}: {e}")
            return None

def main():
    processes = load_processes()
    worker_cycle = cycle(WORKERS)
    results = []

    print(f"Enviando {len(processes)} procesos...")
    for proc in processes:
        worker = next(worker_cycle)
        print(f"Enviando proceso {proc['process_id']} a {worker}")
        result = send_to_worker(worker, proc)
        if result:
            results.append(result)
            print(f"Resultado: {result}")
        time.sleep(0.5)
        
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResultados guardados en: {RESULTS_FILE}")

    print("\n=== RESULTADOS FINALES ===")
    total_wait = sum(r["wait_time"] for r in results)
    avg_wait = total_wait / len(results) if results else 0
    print(f"Tiempo promedio de espera: {avg_wait:.2f}")

if __name__ == "__main__":
    main()