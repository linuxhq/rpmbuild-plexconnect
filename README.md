# rpmbuild-plexconnect

* https://github.com/iBaa/PlexConnect

This respository contains the sources required to build a PlexConnect RPM for RedHat/CentOS

## Sources included

* PlexConnect configuration file for dnsmasq
* PlexConnect configuration file for httpd
* PlexConnect configuration file for nginx
* PlexConnect init script
* PlexConnect log rotation (high output)
* PlexConnect sysconfig configuration file
* PlexConnect spec file
* Certificates for trailers.apple.com 
* Certificates for secure.marketwatch.com
* A modified Settings.cfg

## Requirements

* Apache or Nginx
* Dnsmasq
* Python 2.7
* PlexConnect

## Building the package

First we want to install the necessary 3rd party repositories:

* CentOS 5.x
```sh
rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-5.noarch.rpm
rpm -ivh https://centos5.iuscommunity.org/ius-release.rpm
```

* CentOS 6.x
```sh
rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
rpm -ivh https://centos6.iuscommunity.org/ius-release.rpm
```

* CentOS 7.x
```sh
Nothing to do here as CentOS 7.x comes with Python 2.7
```

Second, install the package dependencies: 

* CentOS 5.x and 6.x
```sh
yum -y install git rpm-build dnsmasq logrotate python27
```

* CentOS 7.x
```sh
yum -y install git rpm-build dnsmasq logrotate python python-pillow
```

Install your webserver of choice

* __Apache__
```sh
yum -y install httpd mod_ssl
```
* __Nginx__
```sh
yum -y install nginx
```

And lastly, check out the git repository and build the package:

```sh
yum -y install rpmdevtools yum-utils
git clone https://github.com/linuxhq/rpmbuild-plexconnect.git rpmbuild
spectool -g -R rpmbuild/SPECS/plexconnect.spec
yum-builddep rpmbuild/SPECS/plexconnect.spec
rpmbuild -ba rpmbuild/SPECS/plexconnect.spec
```

At this point you should see a completed build, so install the package!

```sh
rpm -ivh ${HOME}/rpmbuild/RPMS/noarch/plexconnect-*
```

## Configuring the package

Now that a package has been built, we need to configure the dependent services

__PlexConnect__

* /var/lib/plexconnect/Settings.cfg 
  * (__Optional__) ip_pms: Change this value to your PMS ip if PMS isn't running on the same system
  * (__Optional__) port_pms: Change this value if your PMS isn't running on port 32400 (default)
  * (__Optional__) port_webserver: Leaving this at 8080 is fine, but change it if you have conflicts

__dnsmasq__

* Modify /etc/dnsmasq.conf, and uncomment the following line:
```sh
conf-dir=/etc/dnsmasq.d
```
* Modify /etc/dnsmasq.d/plexconnect.conf, and change x.x.x.x to your servers IP address
* Enable and start the dnsmasq service
```sh
chkconfig dnsmasq on
service dnsmasq start
```

__Apache__
* Modify /etc/httpd/conf.d/plexconnect.conf 
  * (__Optional__) If you changed port_webserver earlier, then update the ProxyPass configuration to match
* Enable and start the httpd service
```sh
chkconfig httpd on
service httpd start
```

__Nginx__
* Modify /etc/nginx/conf.d/plexconnect.conf
  * (__Optional__) If you changed port_webserver earlier, then update the ProxyPass configuration to match
* Enable and start the nginx service
```sh
chkconfig nginx on
service nginx start
```

## Starting the service

```sh
chkconfig plexconnect on
service plexconnect start
```

## Debugging

Logging is set to high (verbose) by default, and the PlexConnect log can be found here: 

* /var/log/plexconnect/PlexConnect.log

## What now?

Now it's time to configure your ATV so it can communicate with PlexConnect.  Instructions can be found here:

* https://github.com/iBaa/PlexConnect/wiki/Install-Guide#setup-your-atv
