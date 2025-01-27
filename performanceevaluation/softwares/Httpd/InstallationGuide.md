# Apache HTTPD Installation Guide

## 1. Download the Source Package
1. Visit the [Apache HTTP Server Official Website](https://httpd.apache.org/).
2. Navigate to the **Download** section.
3. Choose one of the following packages:
   - `httpd-2.4.57.tar.bz2`
   - `httpd-2.4.57.tar.gz`

   > The difference between the two is only the compression format. In this guide, we use `httpd-2.4.57.tar.bz2`.

4. Download the file and transfer it to your Linux environment.

---

## 2. Configure the HTTPD Environment

1. Extract the downloaded file to `/usr/src/`:
   ```bash
   tar xfj httpd-2.4.57.tar.bz2 -C /usr/src/
   ```

2. Remove any pre-installed HTTPD versions to avoid conflicts:
   ```bash
   rpm -e httpd --nodeps
   ```

3. Install the required dependencies:
   ```bash
   sudo apt install -y install apr apr-devel cyrus-sasl-devel expat-devel libdb-devel openldap-devel apr-util-devel apr-util pcre-devel pcre gcc make
   ```

---

## 3. Compile and Install Apache HTTPD

1. Navigate to the extracted directory:
   ```bash
   cd /usr/src/httpd-2.4.57/
   ```

2. Run the configuration script with the desired parameters:
   ```bash
   ./configure --prefix=/usr/local/httpd \
               --enable-so \
               --enable-rewrite \
               --enable-charset-lite \
               --enable-cgi
   ```

   **Explanation of Parameters**:
   - `--prefix`: Specifies the installation directory (`/usr/local/httpd` in this case).
   - `--enable-so`: Enables dynamic module loading for future extensions.
   - `--enable-rewrite`: Enables URL rewriting for site optimization and migration.
   - `--enable-charset-lite`: Adds support for multiple character encodings.
   - `--enable-cgi`: Enables CGI script support for web application extensions.

   > **Note**: Do not switch directories during this process.

3. Compile the source code:
   ```bash
   make
   ```

4. Install the compiled package:
   ```bash
   make install
   ```

   > This step completes the installation of Apache HTTPD.

---

## 4. Post-Installation Optimization

1. The default configuration file is located at:
   ```plaintext
   /usr/local/httpd/conf/httpd.conf
   ```

2. To start the service in the future, navigate to the appropriate directory:
   ```bash
   /usr/local/httpd/bin/httpd -k start
   ```

---

By following these steps, Apache HTTPD will be successfully installed and ready for use on your system.
```