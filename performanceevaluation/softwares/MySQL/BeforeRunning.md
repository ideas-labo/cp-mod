# MySQL-Sysbench.py

Before running this script, there are several specific configuration steps that need to be followed.

The following code snippet shows the key settings:

```python
config_file = "/etc/mysql/conf.d/mysql.cnf"
sys_password = "your password"
confdata = read_csv_to_dict("cp-mod/performanceevaluation/SamplingSet/mysqltest.csv")
outputfile = "./mysqlsysbenchresult.csv"
```

### Explanation of Variables

- **config_file**: This variable represents the path to the `mysql.cnf` configuration file. It is used to specify the location where the MySQL configuration settings are stored.
- **confdata**: This holds the configuration setting data. For detailed information about the data source and its structure, please refer to the `cp-mod/performanceevaluation/SamplingSet` directory.
- **outputfile**: It designates the path where the result file will be saved. This file will contain the outcomes of the operations performed by the script.



Please ensure that you set the above - mentioned variables in the Python file according to your specific environment. This will help the script run correctly and generate accurate results tailored to your MySQL configuration.





# MySQL-tpcc.py

Same with sysbench version.

```python
config_file = "/etc/mysql/conf.d/mysql.cnf"
sys_password = "your password"
confdata = read_csv_to_dict("cp-mod/performanceevaluation/SamplingSet/mysqltest.csv")  
outputfile = "./mysqltpccresult.csv"
```