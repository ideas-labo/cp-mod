## tomcat-ApacheBench.py

Before running this script, there are several specific configuration steps that need to be followed.

The following code snippet shows the key settings:

```python
# Path to tomcat folder
tomcatpath = "/usr/local/tomcat"

resultpath = "/path/to/results"  # Specific a result folder

# Password for sudo commands
password = 'your_password_here'


server_xml_path = f'{tomcatpath}/conf/server.xml'  # Path to Tomcat server.xml
backup_path = '/path/to/backup/server_backup.xml'   # Path for server.xml backup

# Read configuration data from a CSV file (adjust file path as necessary)
confdata = read_csv_to_dict("cp-mod/performanceevaluation/SamplingSet/tomcattest.csv")
```

Please ensure that you set the above - mentioned variables in the Python file according to your specific environment. 



# tomcat-Jmeter.py

```python
# Path to tomcat folder
tomcatpath = "/usr/local/tomcat"

confdata = read_csv_to_dict("cp-mod/performanceevaluation/SamplingSet/nginxtest.csv")

resultpath = "/path/to/results"  # Specific a result folder

# Password for sudo commands
password = 'your_password_here'

# Your nginx path
nginxpath = "/usr/local/nginx-server"

# path to jmeter
JmeterPath = "/usr/local/Jmeter/apache-jmeter-5.6.3/bin/jmeter"

# Read configuration data from a CSV file (adjust file path as necessary)
confdata = read_csv_to_dict("cp-mod/performanceevaluation/SamplingSet/tomcattest.csv")

# Replace with the correct path to your server.xml file and backup location
server_xml_path = f'{tomcatpath}/conf/server.xml'
backup_path = f'{tomcatpath}/server_backup.xml'
```
