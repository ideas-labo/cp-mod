import csv
import subprocess
import numpy as np
import time
import re
import os

password = "your_password"  # Replace with actual password or secure method

# Define different workload parameter combinations
workloads = [
    (10000, 100),
    (10000, 1000),
    (1000, 100),
    (100, 10),
    (100000, 10000)
]

def run_httpd_benchmark(requests, concurrency):
    # Run httpd performance test command
    try:
        command = f"ab -n {requests} -c {concurrency} http://127.0.0.1:70/"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, timeout=120)
    except Exception as e:
        print(e)
        return "error"
    return result.stdout

def extract_data_from_output(output):
    # Regular expressions to match key performance metrics
    requests_per_second_pattern = r"Requests per second:\s+(\d+\.\d+)"
    time_per_request_pattern = r"Time per request:\s+(\d+\.\d+)"

    # Extract metrics
    requests_per_second = re.search(requests_per_second_pattern, output).group(1)
    time_per_request = re.search(time_per_request_pattern, output).group(1)

    return requests_per_second, time_per_request

def clear_httpd_conf(file_path):
    with open(file_path, "w") as file:
        file.truncate()

def startsys():
    try:
        subprocess.run(f"echo {password} | sudo -S {httpdpath}/bin/apachectl start", shell=True, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)
        return False
    time.sleep(2)  # give httpd 2 seconds to start
    return True

def stopsys():
    commandstop = f"echo {password} | sudo -S {httpdpath}/bin/apachectl stop"
    try:
        subprocess.run(commandstop, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)
    time.sleep(1)

def add_config_to_httpd_conf(file_path, configname, configvalue):
    commandwrite2file = f"echo '{configname} {configvalue}' > {file_path}"

    subprocess.run(commandwrite2file, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                   text=True)

    if startsys():
        time.sleep(3)
        return True
    return False

def read_csv_to_dict(filename):
    data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def calculate_change(current, standard):
    """Calculate percentage change."""
    return ((current - standard) / standard) * 100 if standard != 0 else 0

if __name__ == '__main__':
    # Configuration file path
    filepath = "/path/to/httpd.conf"
    # path tp httpd folder
    httpdpath = "/usr/local/httpd/"
    # Read configuration data from a CSV file
    confdata = read_csv_to_dict("cp-mod/performanceevaluation/SamplingSet/httpdtest.csv")

    resultpath = "/path/to/results"

    password = "Your password"




    for requests, concurrency in workloads:
        results_file = f"{resultpath}/Apache-bench-{requests}-{concurrency}.csv"  # Update the path as necessary

        # Check if the result file exists
        if os.path.exists(results_file):
            print(f"Result file for workload {requests}-{concurrency} already exists. Skipping...")
            continue

        print(f"Running workload: {requests} requests, {concurrency} concurrency")

        results = []
        clear_httpd_conf(filepath)

        for conf in confdata:
            stopsys()
            clear_httpd_conf(filepath)
            print(f"{conf['name']} {conf['valuename']} {conf['value']}")

            RPS_list = []
            TPR_list = []

            if not add_config_to_httpd_conf(filepath, conf['name'], conf['value']):
                continue

            for i in range(1, 2):
                bench_output = run_httpd_benchmark(requests, concurrency)
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


            results.append([conf['name'], conf['valuename'], conf['value'], RPS_avg, TPR_avg,])

            # Save results to CSV file
            with open(results_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'ValueName', 'Value', 'Average RPS', 'Average TPR'])
                writer.writerows(results)