# Tomcat Installation and Deployment Guide

## 1. Install Java
### 1.1 Update Package Sources and Search for Java
```bash
sudo apt update
apt search jdk
~~~

Choose `openjdk-8-jdk` from the available options.

### 1.2 Install Java

```bash
sudo apt install openjdk-8-jdk
```

### 1.3 Verify Java Installation

```bash
java -version
```

> Note: The JDK is installed at `/usr/lib/jvm/java-8-openjdk-amd64`. No need to configure environment variables at this step.

------

## 2. Install Tomcat

### 2.1 Download Tomcat

Get the download link from the [Tomcat Official Website](https://tomcat.apache.org/download-80.cgi). Use the following command to download:

```bash
wget https://dlcdn.apache.org/tomcat/tomcat-8/v8.5.75/bin/apache-tomcat-8.5.75.tar.gz
```

### 2.2 Extract Tomcat

Create a target directory and extract the downloaded archive:

```bash
mkdir /usr/local/tomcat
cp apache-tomcat-8.5.75.tar.gz /usr/local/tomcat/
cd /usr/local/tomcat/
tar -zxf apache-tomcat-8.5.75.tar.gz
```

------

## 3. Start Tomcat

### 3.1 Start the Server

Navigate to the extracted directory and start the Tomcat server:

```bash
./apache-tomcat-8.5.75/bin/startup.sh
```

### 3.2 Grant Execution Permission (if required)

If the script cannot be executed, update the permissions:

```bash
chmod -R 755 ./apache-tomcat-8.5.75
./apache-tomcat-8.5.75/bin/startup.sh
```

> If no errors occur, the Tomcat server has started successfully!

------

By following these steps, you can successfully install and deploy Tomcat on Ubuntu 20.04.

```

```