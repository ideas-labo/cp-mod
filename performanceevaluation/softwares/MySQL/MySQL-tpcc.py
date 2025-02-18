import configparser
import subprocess
import re
import csv
import numpy as np

def modify_mysql_config(config_file, section, parameter, value, sys_password):
    try:
        # Create a RawConfigParser object
        config = configparser.RawConfigParser()

        # Grant write permissions
        chmod_777(config_file, sys_password)

        # Read MySQL configuration file
        config.read(config_file)

        # Modify the parameter value
        config.set(section, parameter, value)

        # Save the modified configuration file
        with open(config_file, 'w') as f:
            config.write(f)

        print(f"Successfully modified parameter {parameter} to {value}")

        # Revoke write permissions
        chmod_644(config_file, sys_password)

        # Restart MySQL service
        restart_mysql_service(sys_password)
        return True
    except Exception as error:
        print(f"Modification failed: {error}")
        return False


def restart_mysql_service(sys_password):
    # Use subprocess module to restart MySQL service
    command = f"echo {sys_password} | sudo -S systemctl restart mysql.service"
    subprocess.run(command, shell=True, check=True, executable="/bin/bash")


def chmod_777(file_path, sudo_password):
    # Build chmod command
    command = f"echo {sudo_password} | sudo -S chmod 777 {file_path}"

    # Execute command
    subprocess.run(command, shell=True, check=True, executable="/bin/bash")


def chmod_644(file_path, sudo_password):
    # Build chmod command
    command = f"echo {sudo_password} | sudo -S chmod 644 {file_path}"

    # Execute command
    subprocess.run(command, shell=True, check=True, executable="/bin/bash")


def run_sysbench(mysql_host, mysql_port, mysql_user, mysql_password, mysql_db, threads=8, time=40, report_interval=1, tables=8, table_size=100000):
    commands = {
        "run": f"tpcc_start -h127.0.0.1 -P3306 -d sbtest -u root -p password -w 4 -c 4 -r 3 -l 20",
    }

    for stage, command in commands.items():
        print(f"Starting Sysbench {stage}...")
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            print(result.stdout)
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error log: {e.output}")
            return "error"


def extract_metrics(sysbench_output):
    # Define regular expression pattern for extracting metrics
    TpmC_pattern = r"<TpmC>\s+([\d.]+)\s+TpmC"

    # Extract TpmC value
    TpmC_matches = re.search(TpmC_pattern, sysbench_output)
    TpmC = TpmC_matches.group(1) if TpmC_matches else "Not found"

    return TpmC


def read_csv_to_dict(filename):
    # Read CSV file and convert it into a list of dictionaries
    data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def clearconf(config_file):
    # Clear the MySQL configuration file
    command = f'echo {sys_password} | sudo -S bash -c "echo \'[mysqld]\' > {config_file}"'
    chmod_777(config_file, sys_password)
    subprocess.run(command, shell=True, check=True, executable="/bin/bash")
    chmod_644(config_file, sys_password)




if __name__ == '__main__':

    config_file = "/etc/mysql/conf.d/mysql.cnf"
    sys_password = "your password"  # Replace with actual password or secure method
    confdata = read_csv_to_dict("cp-mod/performanceevaluation/SamplingSet/mysqltest.csv")  # Replace with actual CSV file path
    outputfile = "./mysqltpccresult.csv"


    section = 'mysqld'
    results = []
    for conf in confdata:
        # Clear configuration file
        clearconf(config_file)

        try:

            tps_list = []
            qps_list = []
            latency_list = []

            if not modify_mysql_config(config_file, section, conf['optionname'], conf['value'], sys_password):
                continue

            # Run the benchmark multiple times (adjust loop count as needed)
            for i in range(1, 6):
                sysbench_output = run_sysbench(
                    mysql_host="localhost",
                    mysql_port=3306,
                    mysql_user="root",
                    mysql_password="password",  # Replace with actual password
                    mysql_db="sbtest"
                )
                TpmC = extract_metrics(sysbench_output)
                TpmC = float(TpmC)
                latency_list.append(TpmC)
                print(f"{i}th TpmC: {TpmC} ms")

            results.append([conf['optionname'], conf['valuename'], conf['value'], TpmC])
            with open(outputfile, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(results)

        except Exception as e:
            print(f"---error---: {e}")
            continue
