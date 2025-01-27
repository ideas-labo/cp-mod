import csv
import subprocess
import numpy as np
import time
import re
import shutil
import os
import xml.etree.ElementTree as ET

# Password for sudo commands (this should be handled securely in real applications)
password = '********'

# Define different workload parameters
workloads = [
    (10000, 1000),
    (1000, 10),
]

def run_tomcat_benchmark(requests, concurrency):
    try:
        command = f"ab -n {requests} -c {concurrency} http://localhost:8080/"
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=10)
    except Exception as e:
        print(e)
        return "error"
    return result.stdout

def extract_data_from_output(output):
    requests_per_second_pattern = r"Requests per second:\s+(\d+\.\d+)"
    time_per_request_pattern = r"Time per request:\s+(\d+\.\d+)"

    requests_per_second = re.search(requests_per_second_pattern, output).group(1)
    time_per_request = re.search(time_per_request_pattern, output).group(1)

    return float(requests_per_second), float(time_per_request)

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
        subprocess.run(f"echo {password} | sudo -S /usr/local/tomcat/bin/startup.sh", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)
        return False
    time.sleep(5)  # Allow 5 seconds for Tomcat to start
    return True

def stop_tomcat():
    try:
        subprocess.run(f"echo {password} | sudo -S /usr/local/tomcat/bin/shutdown.sh", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
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
    server_xml_path = '/path/to/tomcat/conf/server.xml'  # Path to Tomcat server.xml
    backup_path = '/path/to/backup/server_backup.xml'   # Path for server.xml backup
    confdata = read_csv_to_dict('/path/to/csv/test.csv')  # Path to configuration data CSV file
    RPS_stand = 0
    TPR_stand = 0

    # Backup the original server.xml file
    backup_server_xml(server_xml_path, backup_path)

    for requests, concurrency in workloads:
        results_file = f"/path/to/results/Apachebench-{requests}-{concurrency}.csv"  # Path to save results

        # Check if result file already exists
        if os.path.exists(results_file):
            print(f"Result file for workload {requests}-{concurrency} already exists. Skipping...")
            continue

        print(f"Running workload: {requests} requests, {concurrency} concurrency")
        results = []

        for conf in confdata:
            stop_tomcat()
            restore_server_xml(server_xml_path, backup_path)
            print(f"Modifying {conf['name']} to {conf['value']}")

            RPS_list = []
            TPR_list = []

            modify_server_xml(server_xml_path, conf['name'], conf['value'])

            if not start_tomcat():
                results.append([conf['name'], conf['valuename'], conf['value'], 'error', 'error', 'error', 'error'])
                continue

            for i in range(1, 6):
                bench_output = run_tomcat_benchmark(requests, concurrency)
                if bench_output == "error":
                    break
                RPS, TPR = extract_data_from_output(bench_output)
                print(f"{i}th : Requests per second: {RPS}, Time per request: {TPR} ms")

                RPS_list.append(RPS)
                TPR_list.append(TPR)

            if bench_output == "error":
                results.append([conf['name'], conf['valuename'], conf['value'], 'timeout', 'timeout', 'timeout', 'timeout'])
                continue

            RPS_list = np.array(RPS_list)
            TPR_list = np.array(TPR_list)

            RPS_avg = np.mean(RPS_list) if len(RPS_list) else None
            TPR_avg = np.mean(TPR_list) if len(TPR_list) else None

            print(f"Average RPS: {RPS_avg}, Average TPR: {TPR_avg} ms")

            results.append([conf['name'], conf['valuename'], conf['value'], RPS_avg, TPR_avg])

        # Save results to CSV file
        with open(results_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'ValueName', 'Value', 'Average RPS', 'Average TPR', 'RPS Change', 'TPR Change'])
            writer.writerows(results)

    # Restore original server.xml file
    restore_server_xml(server_xml_path, backup_path)
    print("Original server.xml restored.")