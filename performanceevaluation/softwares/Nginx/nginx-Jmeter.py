import csv
import subprocess
import numpy as np
import time
import re
import shutil
import os
import xml.etree.ElementTree as ET

# Password for sudo commands
password = 'your_password_here'

# Define different workload parameter combinations
def run_jmeter(sys, id):
    try:
        # Command to run JMeter
        command = f"{JmeterPath} -n -t {JmeterPath}/{sys}/{id}.jmx -l {JmeterPath}/results.jtl -j {JmeterPath}.log"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, timeout=20)
    except Exception as e:
        print(e)
        return "error"
    return result.stdout

def extract_data_from_output(output):
    """Extract throughput value from the JMeter output."""
    throughput_pattern = r"summary =\s+\d+\s+in\s+\d+:\d+:\d+\s+=\s+([\d.]+)/s"
    throughput = re.search(throughput_pattern, output).group(1)
    return float(throughput)

def clear_nginx_conf(file_path):
    # Clear the nginx configuration file
    with open(file_path, "w") as file:
        file.truncate()

def startsys():
    # Start the nginx server
    try:
        subprocess.run(f"echo {password} | sudo -S {nginxpath}/sbin/nginx", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)
        return False
    time.sleep(2)  # give nginx 2 sec to start
    return True

def reloadsys():
    # Reload nginx server
    try:
        subprocess.run(f"echo {password} | sudo -S /{nginxpath}/sbin/nginx -s reload", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)
        return False
    time.sleep(2)  # give nginx 2 sec to reload
    return True

def stopsys():
    # Stop nginx server
    commandstop = f"echo {password} | {nginxpath}/sbin/nginx -s stop"
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
    """Calculate the percentage change."""
    return ((current - standard) / standard) * 100 if standard != 0 else 0

if __name__ == '__main__':
    # Define the path to the configuration file
    filepath = "path_to_nginx.conf"

    confdata = read_csv_to_dict("cp-mod/performanceevaluation/SamplingSet/nginxtest.csv")

    resultpath = "/path/to/results" # Specific a result folder

    # Password for sudo commands
    password = 'your_password_here'

    # Your nginx path
    nginxpath = "/usr/local/nginx-server"

    # path to jmeter
    JmeterPath = "/usr/local/Jmeter/apache-jmeter-5.6.3/bin/jmeter"


    sys = "Nginx"
    for id in range(1, 3):
        results_file = f"{resultpath}/nginx-bench-{id}.csv"
        startsys()
        throughput_list = []
        
        # Run the benchmark 5 times
        for i in range(1, 6):
            bench_output = run_jmeter(sys, id)
            throughput = extract_data_from_output(bench_output)
            throughput_list.append(float(throughput))
        
        throughput_list = np.array(throughput_list)
        throughput_avg = np.mean(throughput_list) if len(throughput_list) else None

        # Check if result file already exists
        if os.path.exists(results_file):
            print(f"Result file for workload {id} already exists. Skipping...")
            continue

        print(f"Running workload: {id}")
        results = []
        clear_nginx_conf(filepath)
        
        # Modify configuration and run benchmarks
        for conf in confdata:
            print(f"Modifying {conf['name']} to {conf['value']}")

            if not add_config_to_nginx_conf(filepath, conf['name'], conf['value']):
                results.append([conf['name'], conf['valuename'], conf['value'], 'error', 'error'])
                continue

            bench_output = run_jmeter(sys, id)
            if bench_output == "error":
                results.append([conf['name'], conf['valuename'], conf['value'], 'timeout', 'timeout'])
                continue

            throughput = extract_data_from_output(bench_output)

            print(f"Throughput: {throughput}")

            throughputchange = calculate_change(throughput, throughput_avg)

            results.append([conf['name'], conf['valuename'], conf['value'], throughput, throughputchange])

            # Save results to CSV file
            with open(results_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'ValueName', 'Value', 'Throughput', 'ThroughputChange'])
                writer.writerows(results)