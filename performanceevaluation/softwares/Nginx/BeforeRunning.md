## nginx-Jmeter.py

Before running this script, there are several specific configuration steps that need to be followed.

The following code snippet shows the key settings:

```python
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
```

Please ensure that you set the above - mentioned variables in the Python file according to your specific environment. 



# nginx-ApacheBench.py

```python
# Set the path for the nginx config file
filepath = "path_to_nginx.conf"
# Your nginx path
nginxpath = "/usr/local/nginx-server"

confdata = read_csv_to_dict("cp-mod/performanceevaluation/SamplingSet/nginxtest.csv")

resultpath = "/path/to/results"  # Specific a result folder
# Password for sudo commands
password = 'your_password_here'
```
