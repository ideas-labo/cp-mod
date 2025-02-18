import csv
import subprocess
import numpy as np
import time
import re
import xml.etree.ElementTree as ET
from datetime import datetime

# Replace with your actual password for sudo operations
password = 'your_password_here'

def read_csv_to_dict(filename):
    data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert each row into a dictionary (column headers as keys)
            data.append(row)
    return data

def run_hibench():
    # Run the Hadoop performance test command
    try:
        # Replace with your actual Hadoop HiBench path
        subprocess.run(f"echo {password} | sudo -S /path/to/HiBench/bin/run_all.sh", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        print(e)

def clear_hadoop_conf(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    for prop in root.findall('property'):
        test = prop.find('test')
        if test is not None:
            root.remove(prop)
    tree.write(file_path, encoding='UTF-8', xml_declaration=True)

def startsys():
    # Replace with the correct command to start your Hadoop system
    commandstart = f"/path/to/hadoop/sbin/start-all.sh"

    try:
        subprocess.run(commandstart, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        print("Hadoop services have been started successfully.")
    except Exception as e:
        print(e)

def stopsys():
    # Replace with the correct command to stop your Hadoop system
    commandstop = f"/path/to/hadoop/sbin/stop-all.sh"

    try:
        subprocess.run(commandstop, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        print("Hadoop services have been stopped successfully.")
    except Exception as e:
        print(e)

def add_config_to_hadoop_conf(file_path, configname, configvalue):
    stopsys()

    tree = ET.parse(file_path)
    root = tree.getroot()

    # Create new <property> element and its child elements
    new_property = ET.SubElement(root, 'property')
    name_element = ET.SubElement(new_property, 'name')
    name_element.text = configname
    value_element = ET.SubElement(new_property, 'value')
    value_element.text = configvalue
    test_element = ET.SubElement(new_property, 'test')
    test_element.text = "test"
    
    # Save the modified XML file
    tree.write(file_path, encoding='UTF-8', xml_declaration=True)

    startsys()

    return True

if __name__ == '__main__':
    # Dictionary to map software to their respective config file paths
    xmlfile = {
        'hdfs': 'hdfs-site.xml',
        'mapreduce': 'mapred-site.xml',
        'yarn': 'yarn-site.xml'
    }


    # Specify the software you want to test : hdfs mapreduce yarn
    software = "mapreduce"
    # Your Hadoop location
    HadoopPath = "/usr/local/hadoop"
    # your Hibench location
    HibenchPath = "/usr/local/hibench"


    # Read configuration data from a CSV file
    confdata = read_csv_to_dict(f"cp-mod/performanceevaluation/SamplingSet/{software}test.csv")

    filepath = f'{HadoopPath}/etc/hadoop/{xmlfile[software]}'

    reportpath = f"{HibenchPath}/report/hibench.report"

    # Start Hadoop services
    startsys()


    for conf in confdata:
        # Clear existing configuration from the Hadoop config file
        clear_hadoop_conf(filepath)

        # Log the configuration change to a report file
        with open(f"{HibenchPath}/report/hibench.report", 'a', encoding='utf-8') as file:
            file.write(f"{conf['name']}|{conf['valuename']}|{conf['value']}\n")
        print(f"{conf['name']}|{conf['valuename']}|{conf['value']}")

        # Add the new configuration to the Hadoop config file
        # add_config_to_hadoop_conf(filepath, conf['name'], conf['value'])

        # Run the HiBench benchmark
        run_hibench()
