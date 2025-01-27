# HiBench Installation and Configuration

## Introduction
HiBench is a benchmarking suite used to evaluate the performance of big data frameworks such as Hadoop, Spark, and others. Below are the steps to install and configure HiBench on your system.

---

## Step 1: Install Java Runtime Environment (JRE) and Development Kit (JDK)

### 1. Install OpenJDK 8
```bash
sudo apt-get install openjdk-8-jre openjdk-8-jdk
```

### 2. Set up environment variables
Edit `.bashrc`:
```bash
vim ~/.bashrc
```
Add:
```bash
# JAVA PATH
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```
Apply changes:
```bash
source ~/.bashrc
```

### 3. Verify Java installation
```bash
java -version
```

---

## Step 2: Install Maven

### Option 1: Direct installation
```bash
sudo apt-get install maven
```

### Option 2: Manual installation
1. Download Maven:
   ```bash
   wget http://apache.fayea.com/maven/maven-3/3.5.0/binaries/apache-maven-3.5.0-bin.zip
   ```
2. Extract:
   ```bash
   unzip apache-maven-3.5.0-bin.zip -d /usr/local/
   ```
3. Set up environment variables:
   Edit `.bashrc`:
   ```bash
   vim ~/.bashrc
   ```
   Add:
   ```bash
   # Maven PATH
   export M3_HOME=/usr/local/apache-maven-3.5.0
   export PATH=$M3_HOME/bin:$PATH
   ```
   Apply changes:
   ```bash
   source ~/.bashrc
   ```

### Verify Maven installation
```bash
mvn -v
```

---

## Step 3: Download HiBench
```bash
git clone https://github.com/intel-hadoop/HiBench.git
```

---

## Step 4: Install HiBench
1. Navigate to the HiBench directory:
   ```bash
   cd HiBench
   ```
2. Build and install desired modules (e.g., for Hadoop SQL testing):
   ```bash
   mvn -Phadoopbench -Dmodules -Psql -Dscala=2.11 clean package
   ```

---

## Step 5: Configure HiBench

### 1. Edit `conf/hadoop.conf`
```properties
# Hadoop home
hibench.hadoop.home             /usr/local/hadoop-2.8.0

# Hadoop executable path
hibench.hadoop.executable       /usr/local/hadoop-2.8.0/bin/hadoop

# Hadoop configuration directory
hibench.hadoop.configure.dir    /usr/local/hadoop-2.8.0/etc/hadoop

# HDFS root path for HiBench data
hibench.hdfs.master             hdfs://localhost:9000/user/hadoop/HiBench

# Hadoop release provider
hibench.hadoop.release          apache
```

### 2. Edit `conf/hibench.conf`
```properties
# Scale profile
hibench.scale.profile           tiny

# Mapper and Reducer parallelism
hibench.default.map.parallelism     8
hibench.default.shuffle.parallelism 8
```

---

## Step 6: Run HiBench

### 1. Start Hadoop services
```bash
start-dfs.sh
start-yarn.sh
```

### 2. Run a workload
```bash
./bin/workloads/micro/wordcount/prepare/prepare.sh
./bin/workloads/micro/wordcount/hadoop/run.sh
```