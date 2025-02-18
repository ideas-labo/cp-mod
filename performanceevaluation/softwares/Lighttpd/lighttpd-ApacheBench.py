import csv
import subprocess
import numpy as np
import time
import re
import os

# System password for sudo access
password = "your_sudo_password"

# Define workload configurations
workloads = [
    (10000, 100),
    (10000, 1000),
    (1000, 100),
    (100, 10),
    (100000, 10000)
]

# Function to run the benchmark with specific requests and concurrency
def run_lighttpd_benchmark(requests, concurrency):
    try:
        command = f"ab -n {requests} -c {concurrency} http://127.0.0.1:70/test.html"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, timeout=10)
    except Exception as e:
        print(e)
        return "error"
    return result.stdout

# Function to extract relevant performance data from the benchmark output
def extract_data_from_output(output):
    lines = output.split('\n')

    # Regular expressions to match key performance indicators
    requests_per_second_pattern = r"Requests per second:\s+(\d+\.\d+)"
    time_per_request_pattern = r"Time per request:\s+(\d+\.\d+)"

    # Extract performance metrics
    requests_per_second = re.search(requests_per_second_pattern, output).group(1)
    time_per_request = re.search(time_per_request_pattern, output).group(1)

    return requests_per_second, time_per_request

# Function to clear the lighttpd configuration file
def clear_lighttpd_conf(file_path):
    with open(file_path, "w") as file:
        file.truncate()

# Function to start the lighttpd service
def startsys():
    try:
        subprocess.run(f"echo {password} | sudo -S {lighttpdpath} -f {filepath}", shell=True, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)
        return False
    time.sleep(2)  # Give lighttpd 2 seconds to start
    return True

# Function to stop the lighttpd service
def stopsys():
    commandstop = f"echo {password} | sudo -S killall lighttpd"

    try:
        subprocess.run(commandstop, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)

# Function to add a configuration value to the lighttpd configuration file
def add_config_to_lighttpd_conf(file_path, configname, configvalue):
    commandwrite2file = f"echo '{configname} = {configvalue}' > {file_path}"

    subprocess.run(commandwrite2file, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    if startsys():
        return True
    return False

# Function to read a CSV file and convert its rows into dictionaries
def read_csv_to_dict(filename):
    data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Function to calculate the percentage change between current and standard values
def calculate_change(current, standard):
    return ((current - standard) / standard) * 100 if standard != 0 else 0

# Main function
if __name__ == '__main__':
    # Configuration file path
    filepath = "/path/to/config/lighttpd.conf"
    # Your lighttpd install folder
    lighttpdpath = "/usr/local/sbin/lighttpd"
    # Read configuration data from a CSV file
    confdata = read_csv_to_dict("cp-mod/performanceevaluation/SamplingSet/lighttpdtest.csv")
    # Specific a result folder
    resultpath = "/path/to/results"

    password = "Your password"

    # Loop through each workload configuration
    for requests, concurrency in workloads:
        results_file = f"{resultpath}/Apache-bench-{requests}-{concurrency}.csv"  # Define the results file

        # Check if the results file already exists, if so, skip
        if os.path.exists(results_file):
            print(f"Result file for workload {requests}-{concurrency} already exists. Skipping...")
            continue

        print(f"Running workload: {requests} requests, {concurrency} concurrency")

        results = []
        clear_lighttpd_conf(filepath)

        # Loop through each configuration in the CSV data
        for conf in confdata:
            stopsys()
            clear_lighttpd_conf(filepath)
            print(f"{conf['name']} {conf['valuename']} {conf['value']}")

            RPS_list = []
            TPR_list = []

            # Add the configuration to the lighttpd configuration file
            if not add_config_to_lighttpd_conf(filepath, conf['name'], conf['value']):
                continue

            # Run the benchmark multiple times
            for i in range(1, 2):
                bench_output = run_lighttpd_benchmark(requests, concurrency)
                if bench_output == "error":
                    break
                RPS, TPR = extract_data_from_output(bench_output)
                print(f"{i}th : Requests per second: {RPS}, Time per request: {TPR} ms")

                RPS_list.append(float(RPS))
                TPR_list.append(float(TPR))

            if bench_output == "error":
                results.append([conf['name'], conf['valuename'], conf['value'], 'timeout', 'timeout'])
                continue

            # Calculate average values
            RPS_list = np.array(RPS_list)
            TPR_list = np.array(TPR_list)

            RPS_avg = np.mean(RPS_list) if len(RPS_list) else None
            TPR_avg = np.mean(TPR_list) if len(TPR_list) else None

            print(f"Average RPS: {RPS_avg}, Average TPR: {TPR_avg} ms")


        # Save the results to a CSV file
        with open(results_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'ValueName', 'Value', 'Average RPS', 'Average TPR'])
            writer.writerows(results)
