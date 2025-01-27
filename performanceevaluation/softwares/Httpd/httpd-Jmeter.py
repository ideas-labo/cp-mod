import csv
import subprocess
import numpy as np
import time
import re
import os

# Password for sudo operations
password = 'password'

# Function to run JMeter test with given system and test ID
def run_jmeter(sys, id):
    try:
        # Command to run JMeter
        command = f"/path/to/jmeter -n -t /path/to/jmeter/{sys}/{id}.jmx -l /path/to/results.jtl -j /path/to/jmeter.log"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, timeout=20)
    except Exception as e:
        print(e)
        return "error"
    return result.stdout

# Function to extract throughput data from JMeter output
def extract_data_from_output(output):
    throughput_pattern = r"summary =\s+\d+\s+in\s+\d+:\d+:\d+\s+=\s+([\d.]+)/s"
    throughput = re.search(throughput_pattern, output).group(1)
    return float(throughput)

# Function to add configuration to a configuration file
def add_config_to_conf(file_path, configname, configvalue):
    commandwrite2file = f"echo '{configname} {configvalue}' > {file_path}"
    subprocess.run(commandwrite2file, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                   text=True)
    # Start the system after modifying the config file
    if start_sys():
        time.sleep(3)
        return True
    return False

# Function to start the system
def start_sys():
    try:
        # Start the system (example using Apache HTTPD)
        subprocess.run(f"echo {password} | sudo -S /path/to/apachectl start", shell=True, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)
        return False
    time.sleep(2)  # Give the system 2 seconds to start
    return True

# Function to stop the system
def stop_sys():
    commandstop = f"echo {password} | sudo -S /path/to/apachectl stop"
    try:
        subprocess.run(commandstop, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)
    time.sleep(1)

# Function to read a CSV file into a dictionary
def read_csv_to_dict(filename):
    data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Function to clear a configuration file by truncating it
def clear_conf(file_path):
    with open(file_path, "w") as file:
        file.truncate()

# Function to calculate percentage change
def calculate_change(current, standard):
    return ((current - standard) / standard) * 100 if standard != 0 else 0

# Main function to run the workload
if __name__ == '__main__':
    filepath = "/path/to/httpd.conf"
    confdata = read_csv_to_dict("/path/to/config.csv")
    sys = "httpd"

    for id in range(1, 3):
        results_file = f"/path/to/results/{sys}-jmeter-{id}.csv"
        
        # Stop the system before starting the test
        stop_sys()
        clear_conf(filepath)
        start_sys()
        
        throughput_list = []
        # Run the benchmark 5 times to get throughput data
        for i in range(1, 6):
            bench_output = run_jmeter(sys, id)
            throughput = extract_data_from_output(bench_output)
            throughput_list.append(float(throughput))
        
        throughput_list = np.array(throughput_list)
        throughput_avg = np.mean(throughput_list) if len(throughput_list) else None

        # Check if results file exists
        if os.path.exists(results_file):
            print(f"Result file for workload {id} already exists. Skipping...")
            continue

        print(f"Running workload: {id}")
        results = []
        clear_conf(filepath)
        
        for conf in confdata:
            stop_sys()
            print(f"Modifying {conf['name']} to {conf['value']}")

            if not add_config_to_conf(filepath, conf['name'], conf['value']):
                results.append([conf['name'], conf['valuename'], conf['value'], 'error', 'error'])
                continue

            bench_output = run_jmeter(sys, id)
            if bench_output == "error":
                results.append([conf['name'], conf['valuename'], conf['value'], 'timeout', 'timeout'])
                continue

            throughput = extract_data_from_output(bench_output)
            print(f"Throughput: {throughput}")

            throughput_change = calculate_change(throughput, throughput_avg)

            results.append([conf['name'], conf['valuename'], conf['value'], throughput, throughput_change])

            # Save the results to a CSV file
            with open(results_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'ValueName', 'Value', 'Throughput', 'ThroughputChange'])
                writer.writerows(results)