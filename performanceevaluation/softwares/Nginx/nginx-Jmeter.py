import csv
import subprocess
import numpy as np
import time
import re
import os

# Define different workload parameter combinations
workloads = [
    (1000, 100),
    (10000, 100),
    (10000, 1000),
    (1000, 10),
]

def run_nginx_benchmark(requests, concurrency):
    # Run nginx performance test command
    try:
        command = f"ab -n {requests} -c {concurrency} http://127.0.0.1:90/test.html"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=10)
    except Exception as e:
        print(e)
        return "error"
    return result.stdout

def extract_data_from_output(output):
    # Use regular expressions to match key performance metrics
    requests_per_second_pattern = r"Requests per second:\s+(\d+\.\d+)"
    time_per_request_pattern = r"Time per request:\s+(\d+\.\d+)"

    # Extract metrics
    requests_per_second = re.search(requests_per_second_pattern, output).group(1)
    time_per_request = re.search(time_per_request_pattern, output).group(1)

    return requests_per_second, time_per_request

def clear_nginx_conf(file_path):
    # Clear the nginx configuration file
    with open(file_path, "w") as file:
        file.truncate()

def startsys():
    # Start the nginx server
    try:
        subprocess.run(f"echo {password} | sudo -S /path/to/nginx-server/sbin/nginx", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)
        return False
    time.sleep(2)  # give nginx 2 sec to start
    return True

def reloadsys():
    # Reload nginx server
    try:
        subprocess.run(f"echo {password} | sudo -S /path/to/nginx-server/sbin/nginx -s reload", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)
        return False
    time.sleep(2)  # give nginx 2 sec to reload
    return True

def stopsys():
    # Stop nginx server
    commandstop = f"echo {password} | /path/to/nginx-server/sbin/nginx -s stop"
    try:
        subprocess.run(commandstop, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)

def add_config_to_nginx_conf(file_path, configname, configvalue):
    # Add configuration to nginx config file
    commandwrite2file = f"echo '{configname} {configvalue};' > {file_path}"
    subprocess.run(commandwrite2file, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # Reload the nginx server to apply changes
    if reloadsys():
        return True
    return False

def read_csv_to_dict(filename):
    # Read a CSV file into a list of dictionaries
    data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def calculate_change(current, standard):
    # Calculate percentage change
    return ((current - standard) / standard) * 100 if standard != 0 else 0

if __name__ == '__main__':
    # Set the path for the nginx config file
    filepath = "/path/to/nginx.conf"
    confdata = read_csv_to_dict("/path/to/newtest.csv")
    



    for requests, concurrency in workloads:
        # Define the result file for the current workload
        results_file = f"/path/to/nginx-bench-{requests}-{concurrency}.csv"

        # Check if the result file already exists
        if os.path.exists(results_file):
            print(f"Result file for workload {requests}-{concurrency} already exists. Skipping...")
            continue

        print(f"Running workload: {requests} requests, {concurrency} concurrency")

        results = []
        clear_nginx_conf(filepath)

        for conf in confdata:
            startsys()
            clear_nginx_conf(filepath)
            print(f"{conf['name']} {conf['valuename']} {conf['value']}")

            RPS_list = []
            TPR_list = []

            # Add the configuration to nginx and reload the server
            if not add_config_to_nginx_conf(filepath, conf['name'], conf['value']):
                results.append([conf['name'], conf['valuename'], conf['value'], 'error', 'error'])
                continue

            # Run the benchmark and extract data
            for i in range(1, 5):
                bench_output = run_nginx_benchmark(requests, concurrency)
                if bench_output == "error":
                    break
                RPS, TPR = extract_data_from_output(bench_output)
                print(f"{i}th : Requests per second:{RPS}, Time per request: {TPR} ms")
                RPS_list.append(float(RPS))
                TPR_list.append(float(TPR))

            if bench_output == "error":
                results.append([conf['name'], conf['valuename'], conf['value'], 'timeout', 'timeout', 'timeout', 'timeout'])
                continue

            RPS_list = np.array(RPS_list)
            TPR_list = np.array(TPR_list)

            RPS_avg = np.mean(RPS_list) if len(RPS_list) else None
            TPR_avg = np.mean(TPR_list) if len(TPR_list) else None

            print(f"Average RPS: {RPS_avg}, Average TPR: {TPR_avg} ms")


            print(f"Average RPS change: {RPSchange}, Average TPR change: {TPRchange}")
            results.append([conf['name'], conf['valuename'], conf['value'], RPS_avg, TPR_avg])

        # Save results to CSV file
        with open(results_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'ValueName', 'Value', 'Average RPS', 'Average TPR', 'RPS Change', 'TPR Change'])
            writer.writerows(results)