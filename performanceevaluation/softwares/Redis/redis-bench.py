import csv
import subprocess
import numpy as np
import time
import os

# Define workload parameter combinations
workloads = [
    ("get", 10000, 50),
    ("set", 10000, 50),
    ("get", 100000, 100),
    ("set", 100000, 100)
]

# Function to run the Redis benchmark
def run_redis_benchmark(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)
        return "error"
    return result.stdout

# Function to extract throughput and latency from benchmark output
def extract_data_from_output(output):
    lines = output.split('\n')
    tps = []
    avg_latency = []

    for i, line in enumerate(lines):
        if 'throughput summary:' in line:
            parts = line.split()
            tps = float(parts[2])

        if 'latency summary (msec)' in line:
            for j in range(i + 1, len(lines)):
                if 'avg' in lines[j]:
                    avg_latency = float(lines[j + 1].split()[0])
                    break

    return tps, avg_latency

# Function to clear the Redis configuration file
def clear_redis_conf(file_path):
    with open(file_path, "w") as file:
        file.truncate()

# Function to add configuration settings to Redis config file
def add_config_to_redis_conf(file_path, configname, configvalue):
    command = f"echo '{configname} {configvalue}' > {filepath}"
    command1 = "redis-cli shutdown"

    with open("/dev/null", "w") as devnull:
        subprocess.run(command1, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        subprocess.Popen(["redis-server", "/path/to/redis/config/redis.conf"], stdout=devnull, stderr=devnull)
    time.sleep(2)  # Give Redis 2 seconds to start

    return True

# Function to read a CSV file into a dictionary
def read_csv_to_dict(filename):
    data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Function to calculate the percentage change from the standard value
def calculate_change(current, standard):
    return ((current - standard) / standard) * 100 if standard != 0 else 0


# Main execution block
if __name__ == '__main__':

    # Redis folder location in your device
    redispath = "/path/to/redis"
    # Configuration file path and data source
    configdatapath = "path/to/config/data"
    # Specific a result folder
    resultpath = "/path/to/results"




    filepath = f"{redispath}/config/redis.conf"

    confdata = read_csv_to_dict(f"{configdatapath}")
    # Loop through the workloads
    for workload_type, num_requests, concurrency in workloads:
        results_file = f"{resultpath}redisbenchmark-{workload_type}-{num_requests}-{concurrency}.csv"

        # Check if the result file already exists
        if os.path.exists(results_file):
            print(f"Result file for workload {workload_type}-{num_requests}-{concurrency} already exists. Skipping...")
            continue

        print(f"Running workload: {workload_type}, requests: {num_requests}, concurrency: {concurrency}")
        results = []

        with open("/dev/null", "w") as devnull:
            subprocess.Popen(["redis-server", filepath], stdout=devnull, stderr=devnull)

        # Loop through each configuration setting
        for conf in confdata:
            clear_redis_conf(filepath)
            print(f"{conf['name']} {conf['valuename']} {conf['value']}")
            try:
                tps_list = []
                latency_list = []

                if not add_config_to_redis_conf(filepath, conf['name'], conf['value']):
                    continue

                # Run benchmark and extract performance data
                for i in range(1, 2):
                    command = f"redis-benchmark -t {workload_type} -n {num_requests} -c {concurrency}"
                    bench_output = run_redis_benchmark(command)

                    if bench_output == "error":
                        break

                    tpss, latencys = extract_data_from_output(bench_output)

                    print(f"Average TPS: {tpss}, Average Latency: {latencys} ms")

                    results.append([conf['name'], conf['valuename'], conf['value'], tpss, latencys])

            except Exception as e:
                print(f"---error---: {e}")
                results.append([conf['name'], conf['valuename'], conf['value'], 'error', 'error'])
                continue

            # Save the results to a CSV file
            with open(results_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'ValueName', 'Value', 'TPS', 'Latency'])
                writer.writerows(results)