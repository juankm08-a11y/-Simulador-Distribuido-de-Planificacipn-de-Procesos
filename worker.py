import socket
import json
import time
import select

def simulate_fcfs(processes):
    wait_time = 0
    total_time = 0
    for p in processes:
        p['arrival'] = 0  # todos llegan al mismo tiempo
        p['start'] = total_time
        p['wait_time'] = p['start'] - p['arrival']
        p['response_time'] = p['start'] + p['burst_time']
        total_time += p['burst_time']
    return processes[0] if processes else None

def main():
    HOST = '0.0.0.0'
    PORT = 9001

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[WORKER] Escuchando en {HOST}:{PORT}")

        while True:
            readable, _, _ = select.select([s], [], [], 1)
            if s in readable:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    if not data:
                        continue
                    try:
                        process = json.loads(data.decode())
                        print(f"[WORKER] Recibido: {process}")

                        result = {
                            "process_id": process["process_id"],
                            "wait_time": 0,  
                            "response_time": process["burst_time"]
                        }

                        conn.sendall(json.dumps(result).encode())
                    except Exception as e:
                        print(f"Error: {e}")

if __name__ == "__main__":
    main()