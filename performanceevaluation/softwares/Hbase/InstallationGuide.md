# HBase Installation Guide

## 1. Install HBase

### 1.1 Download the HBase Package
1. Visit the [official Apache HBase archive](http://archive.apache.org/dist/hbase/) to download the package.  
2. Transfer the downloaded file to your Linux environment.

### 1.2 Extract and Install
1. Extract the package to `/usr/local/`:
   ```bash
   sudo tar -zxf ~/Downloads/hbase- 2.5.5-bin.tar.gz -C /usr/local
   ```

2. Rename the extracted directory:
   ```bash
   cd /usr/local
   sudo mv ./hbase- 2.5.5 ./hbase
   ```

3. Assign ownership to the Hadoop user:
   ```bash
   sudo chown -R hadoop ./hbase
   ```

4. Add HBase to the system PATH:
   ```bash
   vim ~/.bashrc
   ```
   Add the following line at the end:
   ```bash
   export PATH=$PATH:/usr/local/hbase/bin:/usr/local/hadoop/bin:/usr/local/hadoop/sbin
   ```

5. Apply the environment changes:
   ```bash
   source ~/.bashrc
   ```

6. Verify installation:
   ```bash
   cd /usr/local/hbase
   ./bin/hbase version
   ```

---

## 2. Configure HBase for Pseudo-Distributed Mode

### 2.1 Prerequisites
Ensure the following components are installed and configured:
- Hadoop in pseudo-distributed mode
- SSH passwordless login
- JDK configured and added to environment variables

### 2.2 Update `hbase-env.sh`
Edit the `hbase-env.sh` file:
```bash
gedit /usr/local/hbase/conf/hbase-env.sh
```
Uncomment and modify the following lines:
```bash
export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_301
export HBASE_CLASSPATH=/usr/local/hbase/conf
export HBASE_MANAGES_ZK=true
export HBASE_DISABLE_HADOOP_CLASSPATH_LOOKUP="true"
```

### 2.3 Update `hbase-site.xml`
Edit the `hbase-site.xml` file:
```bash
gedit /usr/local/hbase/conf/hbase-site.xml
```
Add the following configuration:
```xml
<configuration>
    <property>
        <name>hbase.rootdir</name>
        <value>hdfs://localhost:9000/hbase</value>
    </property>
    <property>
        <name>hbase.cluster.distributed</name>
        <value>true</value>
    </property>
    <property>
        <name>hbase.unsafe.stream.capability.enforce</name>
        <value>false</value>
    </property>
</configuration>
```

---

## 3. Run and Test HBase

### 3.1 Start HBase
1. **Start SSH Login:**
   ```bash
   ssh localhost
   ```

2. **Start Hadoop Services:**
   ```bash
   cd /usr/local/hadoop
   ./sbin/start-dfs.sh
   ```

3. **Start HBase:**
   ```bash
   cd /usr/local/hbase
   ./bin/start-hbase.sh
   ```

4. **Check Running Processes:**
   Use `jps` to verify running services:
   ```bash
   jps
   ```
   Expected output:
   ```
   7879 Jps
   8093 HMaster
   7777 NameNode
   9031 DataNode
   8765 HRegionserver
   8907 HQuorumPeer
   7654 SecondaryNameNode
   ```

### 3.2 Test HBase
1. **Open HBase Shell:**
   ```bash
   /usr/local/hbase/bin/hbase shell
   ```

2. **Create a Table:**
   ```bash
   create 'student', 'Sname', 'Ssex', 'Sage', 'Sdept', 'course'
   ```

3. **List Tables:**
   ```bash
   list
   ```

4. **Check HBase Status:**
   ```bash
   status
   ```

If all commands execute successfully without errors, your HBase installation is complete and ready to use.
```