# Hadoop-Hibench.py

Before running this script, there are several specific configuration steps that need to be followed.

The following code snippet shows the key settings:

```python
# Specify the software you want to test : hdfs mapreduce yarn
software = "mapreduce"
# Your Hadoop location
HadoopPath = "/usr/local/hadoop"
# your Hibench location
HibenchPath = "/usr/local/hibench"
# Read configuration data from a CSV file
confdata = read_csv_to_dict(f"cp-mod/performanceevaluation/SamplingSet/{software}test.csv")
```

We can see the result in `{HibenchPath}/report/hibench.report`
