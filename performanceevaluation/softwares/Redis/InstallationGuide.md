# Redis Installation and Deployment Guide

### 1. Install Redis

**1.1 Add the Redis Repository and Install Dependencies**

Open your terminal and execute the following commands to install necessary dependencies and add the Redis repository:

```bash
sudo apt install lsb-release curl gpg
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
```

**1.2 Update Package Lists**

After adding the Redis repository, update your package lists:

```bash
sudo apt-get update
```

**1.3 Install Redis**

Proceed to install Redis using the package manager:

```bash
sudo apt-get install redis
```

---

### 2. Using Redis

**2.1 Access the Redis Command-Line Interface (CLI)**

To interact with Redis, enter the CLI by running:

```bash
redis-cli
```

Within the Redis CLI, you can execute various Redis commands. To exit the CLI, simply type:

```bash
exit
```

---

### 3. Managing the Redis Service

**3.1 Start Redis**

You can start the Redis service using one of the following commands:

```bash
sudo /etc/init.d/redis-server start
```

or

```bash
sudo systemctl start redis-server
```

or

```bash
sudo service redis-server start
```

**3.2 Restart Redis**

To restart the Redis service, use:

```bash
sudo service redis-server restart
```

**3.3 Stop Redis**

To stop the Redis service, execute:

```bash
sudo service redis-server stop
```

**3.4 Check Redis Status**

To check the current status of the Redis service:

```bash
sudo service redis-server status
```

---

### 4. Configuring Remote Access

By default, Redis is configured to accept connections only from the localhost. To allow connections from other machines:

**4.1 Modify the Redis Configuration File**

Open the Redis configuration file located at `/etc/redis/redis.conf` with a text editor:

```bash
sudo nano /etc/redis/redis.conf
```

**4.2 Update the Bind Address**

Locate the following line:

```bash
bind 127.0.0.1 -::1
```

Comment it out by adding a `#` at the beginning:

```bash
# bind 127.0.0.1 -::1
```

**4.3 Restart Redis**

After saving the changes, restart the Redis service to apply the new configuration:

```bash
sudo service redis-server restart
```

---

By following these steps, you can successfully install, configure, and manage Redis on an Ubuntu system. 

Redis default configuration file path is  '/etc/redis/redis.conf'