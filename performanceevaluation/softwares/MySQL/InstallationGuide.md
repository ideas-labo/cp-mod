# MySQL Installation Guide



## 1. Prepare the Environment

### 1.1 Install Required Dependencies
```bash
sudo apt-get install -y gcc gcc-c++ ncurses-devel openssl openssl-devel bison bzip2
```

### 1.2 Install gcc-10.2.0
1. Download gcc:
   ```bash
   wget -P /home https://mirrors.aliyun.com/gnu/gcc/gcc-10.2.0/gcc-10.2.0.tar.gz
   ```
2. Extract the package:
   ```bash
   cd /home && tar -xzvf gcc-10.2.0.tar.gz
   ```
3. Configure prerequisites:
   ```bash
   cd /home/gcc-10.2.0 && ./contrib/download_prerequisites
   ```
   > If errors occur, download missing files from [GCC Infrastructure](https://gcc.gnu.org/pub/gcc/infrastructure/).

4. Create installation and build directories:
   ```bash
   mkdir /usr/lib/gcc/x86_64-redhat-linux/10.2.0
   mkdir /home/gcc-build-10.2.0
   cd /home/gcc-build-10.2.0
   ```
5. Configure the build:
   ```bash
   ../gcc-10.2.0/configure --prefix=/usr/lib/gcc/x86_64-redhat-linux/10.2.0/ --enable-checking=release --enable-languages=c,c++ --disable-multilib
   ```
6. Compile and install:
   ```bash
   make && make install
   ```

7. Update GCC:
   ```bash
   mv /usr/bin/gcc /usr/bin/gcc-4.8.5
   mv /usr/bin/g++ /usr/bin/g++-4.8.5
   alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8.5 88 --slave /usr/bin/g++ g++ /usr/bin/g++-4.8.5
   alternatives --install /usr/bin/gcc gcc /usr/lib/gcc/x86_64-redhat-linux/10.2.0/bin/x86_64-pc-linux-gnu-gcc 99 --slave /usr/bin/g++ g++ /usr/lib/gcc/x86_64-redhat-linux/10.2.0/bin/x86_64-pc-linux-gnu-g++
   alternatives --config gcc
   ```
8. Verify installation:
   ```bash
   gcc -v
   ```

9. Update library links:
   ```bash
   rm -f /usr/lib64/libstdc++.so.6
   ln -s /usr/lib/gcc/x86_64-redhat-linux/10.2.0/lib64/libstdc++.so.6 /usr/lib64/libstdc++.so.6
   ```

### 1.3 Install cmake-3.21.3
1. Download CMake from [CMake Download](https://cmake.org/download/).
2. Extract the package:
   ```bash
   tar zxvf cmake-3.21.3.tar.gz
   ```
3. Build and install:
   ```bash
   cd cmake-3.21.3
   ./bootstrap
   gmake
   make install
   ln -s /home/software/cmake-3.21.3/bin/cmake /usr/bin/cmake
   ```
4. Verify installation:
   ```bash
   cmake --version
   ```

---

## 2. Install MySQL

### 2.1 Download MySQL Source Code
Download the MySQL source code with Boost C++ libraries:
```bash
wget https://cdn.mysql.com//Downloads/MySQL-8.0/mysql-boost-8.0.33.tar.gz
```

### 2.2 Create User and Group
```bash
groupadd mysql
useradd -g mysql mysql
```

### 2.3 Extract Source Code
```bash
tar -zxvf mysql-boost-8.0.33.tar.gz
cd mysql-8.0.33
```

### 2.4 Configure Build Parameters
Use `cmake` to configure:
```bash
cmake . -DCMAKE_INSTALL_PREFIX=/home/mysql/mysql-install \
-DMYSQL_DATADIR=/home/mysql/mysql-data \
-DWITH_DEBUG=1 \
-DWITH_BOOST=/home/mysql/mysql-8.0.33/boost \
-DCMAKE_C_COMPILER=/usr/bin/gcc \
-DCMAKE_CXX_COMPILER=/usr/bin/g++ \
-DFORCE_INSOURCE_BUILD=1
```

### 2.5 Compile and Install
Compile and install:
```bash
make
make install
```

---

## 3. Configure MySQL

### 3.1 Edit Configuration File
Create and edit `/etc/my.cnf`:
```ini
[client]
port   = 3306
socket = /home/mysql/mysql-data/mysql.sock

[mysqld]
port = 3306
autocommit = ON
character-set-server = utf8mb4
collation-server = utf8mb4_general_ci
default-storage-engine = INNODB
basedir = /home/mysql/mysql-install
datadir = /home/mysql/mysql-data
socket = /home/mysql/mysql-data/mysql.sock
pid-file = /home/mysql/mysql-data/mysql.pid
log-error = /home/mysql/mysql-data/log/error.log
lower_case_table_names = 1
```

---

## 4. Update Permissions
Set ownership and permissions for directories:
```bash
chown -R mysql:mysql /home/mysql/mysql-data
chmod -R 750 /home/mysql/mysql-data
chown -R mysql:mysql /home/mysql/mysql-install
chmod -R 750 /home/mysql/mysql-install
```

---

## 5. Initialize Database
Initialize the MySQL database:
```bash
bin/mysqld --initialize --user=mysql
```