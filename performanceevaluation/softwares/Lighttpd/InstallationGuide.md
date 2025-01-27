# Lighttpd Installation Guide

## 1. Prepare the Environment
Install the necessary dependencies using the following command:
```bash
yum -y install gcc gcc-c++ gamin gamin-devel
```

---

## 2. Extract the Downloaded Package
Download the `tar.gz` package for Lighttpd from the official website and extract it to a specific directory:
```bash
mkdir /lighttpd
tar -zxvf lighttpd-1.4.tar.gz -C /lighttpd
```

---

## 3. Configure and Compile
Navigate to the extracted directory and run the configuration script:
```bash
cd /lighttpd/lighttpd-1.4/
./configure
```

---

## 4. Install Missing Dependencies
If errors occur during configuration, install the required libraries:

### 4.1 Check for Missing Packages
Identify which package provides `pcre2-config`:
```bash
yum provides "*/pcre2-config"
```

### 4.2 Install Required Packages
Install missing dependencies:
```bash
yum install pcre2-devel-10.23-2.el7.x86_64
yum install zlib-devel -y
```

---

## 5. Build and Install Lighttpd
Run the following commands to compile and install Lighttpd:
```bash
make
make install
```

> Note: Manually compiled installations are not tracked by package managers (e.g., `rpm` or `yum`). You must manually configure and manage the Lighttpd server.

---

## 6. Configure Lighttpd
### 6.1 Create Configuration Directories
```bash
mkdir /etc/lighttpd
```

### 6.2 Copy Configuration Files
Copy the default configuration files:
```bash
cp lighttpd.conf /etc/lighttpd/lighttpd.conf
cp modules.conf /etc/lighttpd
cp -r conf.d/ /etc/lighttpd
```

### 6.3 Update the Configuration File
Edit the `lighttpd.conf` file to bind the server to all network interfaces:
```bash
vi /etc/lighttpd/lighttpd.conf
```
Change:
```plaintext
server.bind = "0.0.0.0"
```

---

## 7. Create a Web Root Directory
Create the default web root directory and add a test file:
```bash
mkdir -p /srv/www/htdocs
echo "hello world" > /srv/www/htdocs/index.html
```

---

## 8. Start Lighttpd
Start the Lighttpd server manually:
```bash
./lighttpd -f /usr/local/sbin/lighttpd
```

---

By following these steps, you will have Lighttpd installed, configured, and running successfully. To access the server, open your browser and navigate to your server's IP address or domain name. 
```

Lighttpd default configuration path is /etc/lighttpd/lighttpd.conf