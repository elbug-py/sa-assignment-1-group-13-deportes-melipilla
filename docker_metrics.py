import csv
import subprocess
import time
import os
import psutil 

OUTPUT_FILE = "metrics_default_1.csv"
INTERVAL = 1

def get_num_cores():
    return psutil.cpu_count(logical=True)

def get_docker_stats():
    """Ejecuta `docker stats --no-stream` y devuelve las líneas."""
    result = subprocess.run(
        ["docker", "stats", "--no-stream", "--format",
         "{{.Container}},{{.Name}},{{.CPUPerc}},{{.MemPerc}},{{.PIDs}}"],
        capture_output=True, text=True
    )
    return result.stdout.strip().split("\n")

def parse_line(line, cores, timestamp):
    parts = line.split(",")
    container = parts[0]
    name = parts[1]
    cpu_raw = float(parts[2].replace("%", "").strip())
    mem = float(parts[3].replace("%", "").strip())
    pids = parts[4].strip()

    # Normalizar CPU: 100% = un core completo
    cpu_normalized = round(cpu_raw / cores, 2)

    return [timestamp, container, name, cpu_normalized, mem, pids]

def main():
    cores = get_num_cores()
    print(f"📊 Detectados {cores} cores. Iniciando logging cada {INTERVAL}s...")

    file_exists = os.path.isfile(OUTPUT_FILE)
    with open(OUTPUT_FILE, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Cabecera si el archivo es nuevo
        if not file_exists:
            writer.writerow(["timestamp", "container", "name", "cpu_percent", "mem_percent", "pids"])

        try:
            while True:
                timestamp = int(time.time())
                lines = get_docker_stats()
                for line in lines:
                    if line.strip():
                        row = parse_line(line, cores, timestamp)
                        writer.writerow(row)
                        print(row)
                time.sleep(INTERVAL)
        except KeyboardInterrupt:
            print("\n⏹️ Logging detenido por el usuario.")

if __name__ == "__main__":
    main()
