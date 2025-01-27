import csv
import subprocess
import numpy as np
import time
import re
import os

# Define password (remove it in the real code for security)
password = 'password_here'


# Function to run JMeter benchmark
def run_jmeter(sys, id):
    try:
        # JMeter command with dynamic arguments
        command = f"/path/to/jmeter/bin/jmeter -n -t /path/to/jmeter/{sys}/{id}.jmx -l /path/to/jmeter/results.jtl -j /path/to/jmeter/jmeter.log"

        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, timeout=20)
    except Exception as e:
        print(e)
        return "error"
    return result.stdout


# Extract throughput data from JMeter output
def extract_data_from_output(output):
    throughput_pattern = r"summary =\s+\d+\s+in\s+\d+:\d+:\d+\s+=\s+([\d.]+)/s"
    throughput = re.search(throughput_pattern, output).group(1)
    return float(throughput)


# Function to modify server configuration file
def add_config_to_conf(file_path, configname, configvalue):
    commandwrite2file = f"echo '{configname} = {configvalue}' > {file_path}"

    subprocess.run(commandwrite2file, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    if start_sys():
        return True
    return False


# Start the server
def start_sys():
    try:
        subprocess.run(f"echo {password} | sudo -S /path/to/lighttpd -f /path/to/config/lighttpd.conf", shell=True, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)
        return False
    time.sleep(2)  # Give lighttpd 2 seconds to start
    return True

# Stop the server
def stop_sys():
    commandstop = f"echo {password} | sudo -S killall lighttpd"

    try:
        subprocess.run(commandstop, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)


# Read CSV file into dictionary
def read_csv_to_dict(filename):
    data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Clear the configuration file
def clear_conf(file_path):
    with open(file_path, "w") as file:
        file.truncate()

# Calculate the percentage change from the standard value
def calculate_change(current, standard):
    return ((current - standard) / standard) * 100 if standard != 0 else 0


# Main execution block
if __name__ == '__main__':
    # Configuration file path and data source
    filepath = "/path/to/config/config.conf"
    confdata = read_csv_to_dict("/path/to/data/config.csv")
    sys = "lighttpd"

    # Loop through test IDs
    for id in range(1, 3):
        results_file = f"/path/to/results/{sys}-jmeter-{id}.csv"
        stop_sys()
        clear_conf(filepath)
        start_sys()
        throughput_list = []
        
        # Run the benchmark 5 times to gather throughput data
        for i in range(1, 6):
            bench_output = run_jmeter(sys, id)
            throughput = extract_data_from_output(bench_output)
            throughput_list.append(float(throughput))
        throughput_list = np.array(throughput_list)
        throughput_avg = np.mean(throughput_list) if len(throughput_list) else None

        # Check if the result file already exists
        if os.path.exists(results_file):
            print(f"Result file for workload {id} already exists. Skipping...")
            continue

        print(f"Running workload: {id}")
        results = []
        clear_conf(filepath)

        # Loop through configuration data
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

            # Save the results to CSV file
            with open(results_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'ValueName', 'Value', 'Throughput', 'ThroughputChange'])
                writer.writerows(results)
