# Hadoop Installation Guide

## 1. Install JDK

1. **Install JDK Using Command**
   On Ubuntu, using a compressed package for JDK installation is complex, as it requires configuring system environment variables and configuration files. For simplicity, install JDK via command:

   Open terminal and run the following command:
   ```bash
   sudo apt-get install openjdk-8-jdk
   ```

2. **Verify Installation**
   After installation, verify using:
   ```bash
   java -version
   ```

3. **Uninstall JDK**
   To remove JDK, run:
   ```bash
   sudo apt remove openjdk*
   ```

4. **Set Up Environment Variables**
   Open the environment file:
   ```bash
   sudo gedit ~/.bashrc
   ```
   Add the following lines at the top of the file:
   ```bash
   export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
   ```
   
   Apply the changes:
   ```bash
   source ~/.bashrc
   ```
   
   Check if JAVA_HOME is set correctly:
   ```bash
   echo $JAVA_HOME
   ```

---

## 2. Install SSH Passwordless Login

1. **Install SSH and OpenSSH Server**
   ```bash
   sudo apt-get install ssh openssh-server
   ```

2. **Generate SSH Key Pair**
   ```bash
   cd ~/.ssh/
   ssh-keygen -t rsa
   ```

3. **Add SSH Key to Authorized Keys**
   ```bash
   cat id_rsa.pub >> authorized_keys
   ```

4. **Test SSH Login**
   Run `ssh localhost` to check if you can log in without a password.

---

## 3. Install Hadoop

### 3.1 Install and Extract Hadoop
1. Download Hadoop from [Tsinghua Mirror](https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-3.3.5/).
2. Upload the `.tar.gz` file to `/usr/local/` and extract:
   ```bash
   tar -zxvf hadoop-3.3.5.tar.gz	/usr/local
   ```

3. Navigate to the extracted folder, rename `hadoop-3.3.5` to `hadoop`, and modify the permissions:
    ```bash
    sudo mv /usr/local/hadoop-3.3.5 /usr/local/hadoop
    sudo chown -R hadoop ./hadoop
    ```

4. Check our Hadoop is available：

   ```bash
   cd /usr/local/hadoop
   ./bin/hadoop version
   ```

### 3.2 Configure Hadoop Files

#### **core-site.xml**
Edit `/usr/local/hadoop/etc/hadoop/core-site.xml` and add:
```xml
<property>
    <name>hadoop.tmp.dir</name>
    <value>file:/usr/local/hadoop-3.3.5/tmp</value>
    <description>Base for other temporary directories.</description>
</property>
<property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
</property>
```

#### **hdfs-site.xml**
Edit `/usr/local/hadoop/etc/hadoop/hdfs-site.xml` and add:
```xml
<property>
    <name>dfs.replication</name>
    <value>1</value>
</property>
<property>
    <name>dfs.namenode.name.dir</name>
    <value>file:/usr/local/hadoop-3.3.5/tmp/dfs/name</value>
</property>
<property>
    <name>dfs.datanode.data.dir</name>
    <value>file:/usr/local/hadoop-3.3.5/tmp/dfs/data</value>
</property>
```

---

## 4. Run Hadoop

1. **Initialize HDFS**
   Run the following command to format the namenode:
   
   ```bash
   bin/hdfs namenode -format
   ```
   
2. **Start NameNode and DataNode**
   Run:
   ```bash
   sbin/start-dfs.sh
   ```

3. **Check Running Processes**
   Use `jps` to check the processes.

   ```bash
   jps
   ```
   
4. **Stop Hadoop**
   Run:
   ```bash
   sbin/stop-dfs.sh
   ```

5. **Access the Web UI**
   Open a browser and go to `http://localhost:9870` to access the Hadoop Web UI.

---


---

## 5. Configure YARN

1. **Check Hostname**
   Run:
   ```bash
   hostname
   ```

2. **Edit `yarn-site.xml`**
   Edit `/etc/hadoop/yarn-site.xml` and add:
   ```xml
   <property>
       <name>yarn.nodemanager.aux-services</name>
       <value>mapreduce_shuffle</value>
   </property>
   <property>
       <name>yarn.resourcemanager.hostname</name>
       <value>liang-VirtualBox</value>
   </property>
   ```

3. **Configure `mapred-site.xml`**
   Edit `/etc/hadoop/mapred-site.xml`:
   
   ```xml
   <property>
       <name>mapreduce.framework.name</name>
       <value>yarn</value>
   </property>
   ```
   
4. **Start YARN**
   Run:
   ```bash
   sbin/start-yarn.sh
   ```

5. **Check Processes**
   Use `jps` to verify that YARN is running.

6. **Access YARN Web UI**
   Open a browser and visit `http://localhost:8088` to access the YARN ResourceManager Web UI.

---

By following these steps, you will have Hadoop successfully installed and configured on your system.
