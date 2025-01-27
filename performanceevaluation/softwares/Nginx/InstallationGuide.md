# Nginx Installation and Deployment Guide

## 1. Preparation
Before installing Nginx, ensure your system is updated and has the necessary dependencies.

### 1.1 Update System Packages
```bash
sudo apt update
sudo apt upgrade
```

### 1.2 Install Dependencies
Install required dependencies to ensure Nginx runs smoothly:
```bash
sudo apt install -y curl gnupg2 ca-certificates lsb-release
```

---

## 2. Install Nginx
Use the `apt` package manager to install Nginx on Ubuntu 22.04.

### 2.1 Install Nginx
```bash
sudo apt install -y nginx
```

### 2.2 Start Nginx Service
Start the Nginx service:
```bash
sudo systemctl start nginx
```

### 2.3 Enable Nginx at Startup
Ensure Nginx starts automatically on system boot:
```bash
sudo systemctl enable nginx
```

---

## 3. Nginx Configuration

### 3.1 Modify Default Configuration
The main configuration file is located at `/etc/nginx/nginx.conf`. You can edit it to modify default behavior.

To modify the default virtual host:
```bash
sudo nano /etc/nginx/sites-available/default
```
Adjust settings such as the root directory or `server_name`. After making changes, reload Nginx to apply them:
```bash
sudo systemctl reload nginx
```

### 3.2 Add a New Virtual Host
Create a new configuration file for a virtual host:
```bash
sudo nano /etc/nginx/sites-available/mywebsite
```
Add the following content:
```nginx
server {
    listen 80;
    server_name mywebsite.com www.mywebsite.com;

    location / {
        root /var/www/mywebsite;
        index index.html;
    }
}
```
Create a symbolic link to enable the configuration:
```bash
sudo ln -s /etc/nginx/sites-available/mywebsite /etc/nginx/sites-enabled/
```
Reload Nginx to apply changes:
```bash
sudo systemctl reload nginx
```

---

## 4. Managing Nginx Service

### 4.1 Start, Stop, and Restart Nginx
Start the Nginx service:
```bash
sudo systemctl start nginx
```
Stop the Nginx service:
```bash
sudo systemctl stop nginx
```
Restart the Nginx service:
```bash
sudo systemctl restart nginx
```

### 4.2 Check Nginx Status
To view the current status of Nginx:
```bash
sudo systemctl status nginx
```

### 4.3 View Logs
Error logs are located at `/var/log/nginx/error.log`. Use the following command to view them:
```bash
sudo tail -f /var/log/nginx/error.log
```

---

## 5. Deploying a Static Website

### 5.1 Create a Directory for the Website
```bash
sudo mkdir -p /var/www/mywebsite
```

### 5.2 Copy Website Files
Copy your static website files to the created directory:
```bash
sudo cp /path/to/your/website/* /var/www/mywebsite/
```

### 5.3 Configure Nginx for the Website
Edit the Nginx configuration file for your website:
```bash
sudo nano /etc/nginx/sites-available/mywebsite
```
Add the following configuration:
```nginx
server {
    listen 80;
    server_name mywebsite.com www.mywebsite.com;

    location / {
        root /var/www/mywebsite;
        index index.html;
    }
}
```
Enable the configuration and reload Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/mywebsite /etc/nginx/sites-enabled/
sudo systemctl reload nginx
```

You can now access your static website by entering your server's IP address or domain name in a browser.
```

The main configuration file is located at `/etc/nginx/nginx.conf`.