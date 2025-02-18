# Hbase-YCSB.py

Before running this script, there are several specific configuration steps that need to be followed.

The following code snippet shows the key settings:

```python
# Replace with your actual YCSB home directory path
YCSB_HOME = "/path/to/ycsb"
# Replace with your actual Hadoop config file path
confdata = read_csv_to_dict("/cp-mod-icse2025/cp-mod/performanceevaluation/SamplingSet/hbasetest.csv")
# hbase path
hbasepath = "/path/to/hbase"
# config file path
filepath = f'{hbasepath}/conf/hbase-site.xml'

resultpath = "/resultpath"

password = " your password"
```

Please ensure that you set the above - mentioned variables in the Python file according to your specific environment. 
