import csv
import subprocess
import xml.etree.ElementTree as ET
import re

# Replace with your actual password for sudo operations
password = 'your_password_here'

def read_csv_to_dict(filename):
    data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def run_command(command, timeout=None):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=timeout)
        print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}\n{e.output}")
        return None
    except subprocess.TimeoutExpired as e:
        print(f"Command timed out: {command}\n{e.output}")
        return None

def create_hbase_table():
    commands = '''
    # create your table
    '''
    process = subprocess.Popen(['hbase', 'shell'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        stdout, stderr = process.communicate(commands, timeout=20)
        print(stdout)
        if process.returncode != 0:
            print(f"Error creating HBase table: {stderr}")
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        print(f"Command timed out while creating HBase table: {stderr}")

def load_data():
    # Replace with your YCSB home directory path
    command = f"{YCSB_HOME}/bin/ycsb load hbase20 -cp /etc/hbase/conf/ -p columnfamily=cf -P {YCSB_HOME}/workloads/workload"
    run_command(command, timeout=20)

def run_ycsb():
    # Replace with your YCSB home directory path
    command = f"{YCSB_HOME}/bin/ycsb run hbase20 -cp /etc/hbase/conf/ -p columnfamily=cf -p recordcount= -p operationcount= -P {YCSB_HOME}/workloads/workload -threads "
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=20)
        print("Command executed successfully:")
        runtime, throughput = parse_and_store_output(result.stdout)
        print(runtime, throughput)
        return runtime, throughput
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error output: {e.stderr}")
        return "0", "0"
    except subprocess.TimeoutExpired as e:
        print(f"Command timed out: {command}")
        return "0", "0"

def parse_and_store_output(output):
    runtime_pattern = r'\[OVERALL\], RunTime\(ms\), (\d+)'
    throughput_pattern = r'\[OVERALL\], Throughput\(ops/sec\), ([\d.]+)'

    runtime_match = re.search(runtime_pattern, output)
    throughput_match = re.search(throughput_pattern, output)

    if runtime_match and throughput_match:
        runtime = runtime_match.group(1)
        throughput = throughput_match.group(1)
        return runtime, throughput
    else:
        return "0", "0"

def clear_hadoop_conf(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    for prop in root.findall('property'):
        test = prop.find('test')
        if test is not None:
            root.remove(prop)
    tree.write(file_path, encoding='UTF-8', xml_declaration=True)

def start_hbase():
    # Replace with the correct command to start HBase
    command = f"{hbasepath}/bin/start-hbase.sh"
    run_command(command, timeout=20)

def stop_hbase():
    # Replace with the correct command to stop HBase
    command1 = "hbase-daemon.sh stop master"
    command2 = f"/{hbasepath}/bin/stop-hbase.sh"
    run_command(command1, timeout=10)
    run_command(command2, timeout=20)

def add_config_to_hadoop_conf(file_path, configname, configvalue):
    stop_hbase()
    tree = ET.parse(file_path)
    root = tree.getroot()
    new_property = ET.SubElement(root, 'property')
    name_element = ET.SubElement(new_property, 'name')
    name_element.text = configname
    value_element = ET.SubElement(new_property, 'value')
    value_element.text = configvalue
    test_element = ET.SubElement(new_property, 'test')
    test_element.text = "test"
    tree.write(file_path, encoding='UTF-8', xml_declaration=True)
    start_hbase()
    return True

def write_results_to_csv(results):
    # Write results to CSV file (adjust path as needed)
    with open(f"{resultpath}/result.csv", 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        writer.writerow(['conf_name', 'conf_valuename', 'conf_value', 'runtime', 'throughput'])

        # Write each configuration and result as a row
        for row in results:
            writer.writerow(row)

if __name__ == '__main__':
    # Replace with your actual YCSB home directory path
    YCSB_HOME = "/path/to/ycsb"
    # Replace with your actual Hadoop config file path
    confdata = read_csv_to_dict("/cp-mod-icse2025/cp-mod/performanceevaluation/SamplingSet/hbasetest.csv")

    hbasepath = "/path/to/hbase"

    filepath = f'{hbasepath}/conf/hbase-site.xml'

    resultpath = "/resultpath"

    password = " your password"

    # Store all results
    results = []
    start_hbase()
    for conf in confdata:
        clear_hadoop_conf(filepath)
        print(f"Configuring: {conf['name']}|{conf['valuename']}|{conf['value']}")
        add_config_to_hadoop_conf(filepath, conf['name'], conf['value'])

        # Create HBase table
        try:
            create_hbase_table()    

            # Load data
            load_data()

        except:
            results.append([f"{conf['name']}|{conf['valuename']}|{conf['value']}", "error", "error"])
            continue

        # Run YCSB test and get results
        runtime, throughput = run_ycsb()

        # Store the configuration and test results in one row
        results.append([f"{conf['name']}|{conf['valuename']}|{conf['value']}", runtime, throughput])

        # Write all results to CSV file
        write_results_to_csv(results)

        print("YCSB test results have been successfully written to CSV.")
