| Workload | MySQL      | Lighttpd     | Httpd        | Nginx        | Redis          | Yarn    | HDFS    | Mapreduce | Hbase | Tomcat       |
| -------- | ---------- | ------------ | ------------ | ------------ | -------------- | ------- | ------- | --------- | ----- | ------------ |
| W1       | sysbench-10000-4-16-20-10000 | Apache bench- 10000-100 | Apache bench- 10000-100 | Apache bench- 10000-100 | redisbenchmark-get-10000-50 | HiBench-micro.sort | HiBench-micro.sortHiBench | HiBench-micro.sortHiBench | YCSB-100000-100000-workloadb | Apache bench-10000-100 |
| W2       | sysbench-8-8-40-1000 | Apache bench-10000-1000 | Apache bench-10000-1000 | Apache bench-10000-1000 | redisbenchmark-set-10000-50redisbenchmark | HiBench-micro.terasortHiBench | HiBench-micro.terasortHiBench | HiBench-micro.terasortHiBench | YCSB-1000-1000-workloada | Apache bench-10000-1000 |
| W3       | TPC-C -w2 -1-3-10 | JMeter-100-10 | JMeter-200-15 | JMeter-100-10 | redisbenchmark-get-100000-100redisbenchmark | HiBench-micro.wordcountHiBench | HiBench-micro.wordcountHiBench | HiBench-micro.wordcountHiBench | YCSB-10000-10000-workloadc   | Apache bench-1000-10 |
| W4       | TPC-C -w4 -4-3-20 | NA           | NA           | NA           | NA             | NA      | NA      | NA        | NA    | NA           |





### Specific instructions

| Workload | MySQL                                           | Lighttpd                                            | Httpd                                               | Nginx                                               | Redis                   | Yarn                    | HDFS                    | Mapreduce               | Hbase                   | Tomcat              |
| -------- | ----------------------------------------------- | --------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------- | ----------------------- | ----------------------- | ----------------------- | ----------------------- | ----------------------- | ------------------- |
| W1       | threads=4, time=16, tables=20, table_size=10000 | ab -n 10000 -c 100                                  | ab -n 10000 -c 100                                  | ab -n 10000 -c 100                                  | -t get -n 10000 -c 50   | HiBench-micro.sort      | HiBench-micro.sort      | HiBench-micro.sort      | 100000-100000-workloadb | ab -n 10000 -c 100  |
| W2       | threads=8, time=8, tables=40, table_size=1000   | ab -n 10000 -c 1000                                 | ab -n 10000 -c 1000                                 | ab -n 10000 -c 1000                                 | -t set -n 10000 -c 50   | HiBench-micro.terasort  | HiBench-micro.terasort  | HiBench-micro.terasort  | 1000-1000-workloada     | ab -n 10000 -c 1000 |
| W3       | -w 2 -c 1 -r 3 -l 10                            | ThreadGroup.num_threads:100 LoopController.loops:10 | ThreadGroup.num_threads:200 LoopController.loops:15 | ThreadGroup.num_threads:100 LoopController.loops:10 | -t get -n 100000 -c 100 | HiBench-micro.wordcount | HiBench-micro.wordcount | HiBench-micro.wordcount | 10000-10000-workloadc   | ab -n 1000 -c 100   |
| W4       | -w 4 -c 4 -r 3 -l 20                            | NA                                                  | NA                                                  | NA                                                  | NA                      | NA                      | NA                      | NA                      | NA                      | NA                  |



### Explanation of  instruction parameters

#### Sysbench

**threads**: number of threads to use 

**time**: limit for total execution time in seconds 

**tablesize**: N number of rows per table 

**tables**: number of N tables 



#### TPC-C
**w**: |WAREHOUSES| 
**c**: |CONNECTIONS|
**r**: |WARMUP TIME| 
**l**: |BENCHMARK TIME|



#### Apache bench

**n** requests Number of requests to perform

**c** concurrency Number of multiple requests to make



####   JMeter

**ThreadGroup.num_threads**: Number of thread groups, also known as parallel numbers

**LoopController.loops**: Set the number of runs



#### redisbenchmark

**-t** : Only run the comma-separated list of tests

**-c** : Number of parallel connections 

**-n** : Total number of requests 



#### YCSB

**recordcount**: The number of records loaded into the database during the load phase; 

**operationcount**: The data range of the run phase operation. The total number of operations performed during the run phase



#### Hibench

**wordcount**: This workload counts the occurrence of each word in the input data, which are generated using RandomTextWriter. It is representative of another typical class of real world MapReduce jobs - extracting a small amount of interesting data from large data set.

**sort**: This workload sorts its text input data, which is generated using RandomTextWriter.

**terasort**: TeraSort is a standard benchmark created by Jim Gray. Its input data is generated by Hadoop TeraGen example program.