## lighttpd-ApacheBench.py

Before running this script, there are several specific configuration steps that need to be followed.

The following code snippet shows the key settings:

```python
# Configuration file path
filepath = "/path/to/config/lighttpd.conf"
# Your lighttpd install folder
lighttpdpath = "/usr/local/sbin/lighttpd"
# Read configuration data from a CSV file
confdata = read_csv_to_dict("cp-mod/performanceevaluation/SamplingSet/lighttpdtest.csv")
# Specific a result folder
resultpath = "/path/to/results"  

password = "Your password"
```

Please ensure that you set the above - mentioned variables in the Python file according to your specific environment. 



# lighttpd-Jmeter.py

```python
# Configuration file path
filepath = "/path/to/config/lighttpd.conf"
# Your lighttpd install folder
lighttpdpath = "/usr/local/sbin/lighttpd"
# Read configuration data from a CSV file
confdata = read_csv_to_dict("cp-mod/performanceevaluation/SamplingSet/lighttpdtest.csv")
# Specific a result folder
resultpath = "/path/to/results"  

password = "Your password"
```
