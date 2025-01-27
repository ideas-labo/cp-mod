# YCSB Installation and Deployment Guide

## 1. Overview
YCSB (Yahoo! Cloud Serving Benchmark) is a benchmarking tool that provides advanced workload templates for performance testing. Compared to HBase's built-in PE tool, YCSB offers greater flexibility and supports multi-threaded tests and customizable workloads.

---

## 2. Installation

### 2.1 Global Configuration
Set the following environment variables:
```bash
hbaseYcsbUrl="https://github.com/brianfrankcooper/YCSB/releases/download/0.17.0/ycsb-hbase20-binding-0.17.0.tar.gz"
hbaseYcsbPkg=$(basename $hbaseYcsbUrl)
hbaseYcsbDir=$(basename $hbaseYcsbUrl ".tar.gz")
export YCSB_HOME="/opt/$hbaseYcsbDir"
```

### 2.2 Download YCSB
1. Download the YCSB package:
   ```bash
   wget $hbaseYcsbUrl -P /tmp/
   ```
2. Extract the package:
   ```bash
   sudo tar -xzf /tmp/$hbaseYcsbPkg -C /opt
   ```
3. Verify installation:
   ```bash
   $YCSB_HOME/bin/ycsb -h
   ```

---

## 3. Configuration

### 3.1 Create a Table in HBase
Run the following script in the HBase shell to create a table:
```bash
cat << EOF | hbase shell
disable 'usertable'
drop 'usertable'
n_splits = 30 # Adjust based on your number of regionservers
create 'usertable', 'cf', {SPLITS => (1..n_splits).map {|i| "user#{1000+i*(9999-1000)/n_splits}"}}
describe 'usertable'
EOF
```

### 3.2 Load Data
Use the `workloada` template to load data:
```bash
$YCSB_HOME/bin/ycsb load hbase20 \
    -cp /etc/hbase/conf/ \
    -p columnfamily=cf \
    -P $YCSB_HOME/workloads/workloada
```

**Key Parameters:**
- `recordcount`: Total number of records to insert (not included in `operationcount`).
- `operationcount`: Total number of operations (e.g., read, update, scan, insert).

For example:
```bash
-p recordcount=10000 -p operationcount=10000
```

### 3.3 Verify Data
Verify that data has been successfully loaded into the table:
```bash
cat << EOF | hbase shell
scan 'usertable'
EOF
```

---

## 4. Workloads Overview

YCSB provides six predefined workload templates stored in `$YCSB_HOME/workloads`:

| **Workload** | **Description** |
|--------------|-----------------|
| `workloada`  | 50% reads, 50% updates (balanced read/write) |
| `workloadb`  | 95% reads, 5% updates (read-heavy) |
| `workloadc`  | 100% reads |
| `workloadd`  | 95% reads, 5% inserts (recently updated records are accessed more frequently) |
| `workloade`  | 95% scans, 5% inserts (small range queries) |
| `workloadf`  | 50% reads, 50% read-modify-write operations |

---

## 5. Running the Benchmark

1. Choose the appropriate workload template based on your requirements.
2. Run the benchmark using the following command (example with `workloadb`):
   ```bash
   nohup $YCSB_HOME/bin/ycsb run hbase20 \
       -cp /etc/hbase/conf/ \
       -p columnfamily=cf \
       -p recordcount=10000000 \
       -p operationcount=10000000 \
       -P $YCSB_HOME/workloads/workloadb \
       -threads 3 \
       -s &> nohup.out &
   ```
3. Monitor the progress:
   ```bash
   tail -f nohup.out
   ```

---

## 6. Report and Analysis

After the benchmark completes, YCSB generates a detailed report that includes metrics such as throughput, latency, and operation types.

By following the steps above, you can successfully install, configure, and run YCSB to benchmark HBase performance under various workloads.
```