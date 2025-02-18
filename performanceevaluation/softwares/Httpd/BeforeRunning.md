## httpd-ApacheBench.py

Before running this script, there are several specific configuration steps that need to be followed.

The following code snippet shows the key settings:

```python
# Configuration file path
filepath = "/path/to/httpd.conf"
# path tp httpd folder
httpdpath = "/usr/local/httpd/"
# Read configuration data from a CSV file
confdata = read_csv_to_dict("cp-mod/performanceevaluation/SamplingSet/httpdtest.csv")
# Specific a result folder
resultpath = "/path/to/results"  

password = "Your password"
```

Please ensure that you set the above - mentioned variables in the Python file according to your specific environment. 

nginx-ApacheBench

nginx-Jmeter.py

# httpd-Jmeter.py

```python
# path tp httpd folder
httpdpath = "/usr/local/httpd/"
# Configuration file path
filepath = "/path/to/httpd.conf"
# Read configuration data from a CSV file
confdata = read_csv_to_dict("cp-mod/performanceevaluation/SamplingSet/httpdtest.csv")
# path to jmeter
JmeterPath = "/usr/local/Jmeter/apache-jmeter-5.6.3/bin/jmeter"

resultpath = "/path/to/results"

password = "Your password"
```
