# SAMI

An openstack swift administrative management interface.

## Prerequisites

* A working Swift cluster.
* A working Keystone Node.
* A web server.

## Installation

Unpack SAMI to your html directory.

## Configuration

### 1. Permissions

Give your web server permissions to access swift.

#### Step 1

Add the web server user to sudoers list.

* sudo visudo

#### Step 2

Add the line:

* [INSERT-WEB-SERVER-USER] ALL=(ALL) NOPASSWD: /bin/chmod 710 /etc/swift/, /usr/bin/swift-ring-builder

For example, if you run apache, [INSERT-WEB-SERVER-USER] = www-data.

### 2. Initialize settings.conf

#### In order for SAMI to interact with Swift and Keystone, it must have the following parameters:

* KEYSTONE-ADMIN-TOKEN (The Keystone admin token)
* KEYSTONE-ENDPOINT (The Keystone endpoint)
* SUPER-USER (The admin user name, which was previously created in keystone)
* SUPER-USER-PASSWORD (The admin user password)
* ADMIN-ID (The admin id)
* ADMIN-ROLE-ID (The admin role ID, which role-name must also be specified in swift)
* USER-ROLE-NAME (The user role name)
* CAPACITY-WARNING-THRESHHOLD (The % warning threshold to alert you)
* CAPACITY-ERROR-THRESHOLD (The total cluster capacity % error threshold for alerting)
* EMAIL-USER-ADDRESS (The email address to send email alerts from)
* EMAIL-USER-PASSWORD (The email password)
* EMAIL-SERVER (The mail server used to deal with requests)
* EMAIL-ALERT-RECIPIENTS (The recipients to alert via email)

#### Example settings.conf (Each bullet represents a line in the conf file):

* DO NOT CHANGE THE FORMAT OF THIS FILE
* Each line represents a value in the following format:
* KEYSTONE-ADMIN-TOKEN, KEYSTONE-ENDPOINT, SUPER-USER, SUPER-USER-PASSWORD, ADMIN-ID, ADMIN-ROLE-ID, USER-ROLE-NAME, CAPACITY-WARNING-THRESHHOLD, CAPACITY-ERROR-THRESHOLD, EMAIL-USER-ADDRESS, EMAIL-USER-PASSWORD, EMAIL-SERVER, EMAIL-ALERT-RECIPIENTS
* ADMIN
* http://10.27.121.15:35357/v2.0/
* admin
* secrete
* 2170679e715a4b4095d0d45e92adbe7c
* e456c93bcd924fb89847509144a9e77c
* swiftuser
* 75
* 85
* nobody@gmail.com
* emailpass123
* recipient1@email.com, recipient2@email.com

### 3. Start Cron Jobs

#### Step 1

Edit the sudo crontab file.

* sudo crontab -e

#### Step 2

Set up the cron jobs (in this example, run hourly).

* 0 * * * * /your-SAMI-location/alerting.py
* 30 * * * * /your-SAMI-location/emailalerts.py

Note that you should not run these jobs at the same time for performance reasons.
