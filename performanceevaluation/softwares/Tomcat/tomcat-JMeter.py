import csv
import subprocess
import numpy as np
import time
import re
import shutil
import os
import xml.etree.ElementTree as ET

# Replace with your actual password for sudo operations
password = 'your_password_here'

# Define different workload parameter combinations
def run_tomcat_benchmark(id):
    try:
        # Replace with the correct path to your JMeter installation and test files
        command = f"/path/to/jmeter -n -t /path/to/tomcat/{id}.jmx -l /path/to/results.jtl -j /path/to/jmeter.log"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=10)
    except Exception as e:
        print(e)
        return "error"
    return result.stdout

def extract_data_from_output(output):
    # Regex pattern to extract throughput value from JMeter output
    throughput_pattern = r"summary =\s+\d+\s+in\s+\d+:\d+:\d+\s+=\s+([\d.]+)/s"
    throughput = re.search(throughput_pattern, output).group(1)
    return float(throughput)

def backup_server_xml(server_xml_path, backup_path):
    shutil.copy(server_xml_path, backup_path)

def restore_server_xml(server_xml_path, backup_path):
    shutil.copy(backup_path, server_xml_path)

def modify_server_xml(server_xml_path, attribute, new_value):
    tree = ET.parse(server_xml_path)
    root = tree.getroot()
    connector = root.find('.//Connector')
    
    if connector is not None:
        connector.set(attribute, new_value)

    tree.write(server_xml_path, encoding='utf-8', xml_declaration=True)

def start_tomcat():
    try:
        # Replace with your Tomcat startup command and correct password handling
        subprocess.run(f"echo {password} | sudo -S /path/to/tomcat/bin/startup.sh", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)
        return False
    time.sleep(5)  # Allow Tomcat 5 seconds to start
    return True

def stop_tomcat():
    try:
        # Replace with your Tomcat shutdown command and correct password handling
        subprocess.run(f"echo {password} | sudo -S /path/to/tomcat/bin/shutdown.sh", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)

def read_csv_to_dict(filename):
    data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def calculate_change(current, standard):
    return ((current - standard) / standard) * 100 if standard != 0 else 0

if __name__ == '__main__':
    # Replace with the correct path to your server.xml file and backup location
    server_xml_path = '/path/to/tomcat/conf/server.xml'
    backup_path = '/path/to/tomcat/server_backup.xml'

    # Read configuration data from a CSV file (adjust file path as necessary)
    confdata = read_csv_to_dict('/path/to/tomcat/test.csv')
    
    start_tomcat()

    # Backup the original server.xml file
    backup_server_xml(server_xml_path, backup_path)

    for id in range(1, 3):
        # Replace with your actual results file path
        results_file = f"/path/to/tomcat/tomcat-jmeter-{id}.csv"
        
        throughput_list = []
        for i in range(1, 6):
            # Run JMeter benchmark and extract throughput data
            bench_output = run_tomcat_benchmark(id)
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

        for conf in confdata:
            stop_tomcat()
            restore_server_xml(server_xml_path, backup_path)
            print(f"Modifying {conf['name']} to {conf['value']}")

            modify_server_xml(server_xml_path, conf['name'], conf['value'])

            if not start_tomcat():
                results.append([conf['name'], conf['valuename'], conf['value'], 'error'])
                continue

            bench_output = run_tomcat_benchmark(id)
            if bench_output == "error":
                results.append([conf['name'], conf['valuename'], conf['value'], 'timeout'])
                continue

            throughput = extract_data_from_output(bench_output)
            print(f"throughput: {throughput}")

            results.append([conf['name'], conf['valuename'], conf['value'], throughput])

        # Save results to CSV file
        with open(results_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'ValueName', 'Value', 'throughput'])
            writer.writerows(results)

    # Restore the original server.xml file
    restore_server_xml(server_xml_path, backup_path)
    print("Original server.xml restored.")