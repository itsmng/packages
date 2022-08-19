%global useselinux 1

%global tarname itsm-ng
%global official_version 1.2.0

Name:           itsm-ng
Version:        1.2.0
Release:        1%{?dist}
Summary:        IT Equipment Manager

Group:       Applications/Internet
License:     GPLv2
URL:         http://www.itsm-ng.org/
Source0:     %{name}-%{version}.tgz

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       mariadb-server
Requires:       httpd
Requires:       php
Requires:       php-sodium
Requires:       php-ctype
Requires:       php-curl
Requires:       php-gd
Requires:       php-iconv
Requires:       php-intl
Requires:       php-json
Requires:       php-mbstring
Requires:       php-mysqli
Requires:       php-simplexml
Requires:       php-ldap
Requires:       php-apcu
Requires:       php-xmlrpc
Requires:       php-opcache

%undefine __brp_mangle_shebangs

%description
ITSM-NG application RPM package

%prep
%setup -q -n %{name}

%install
mkdir -p %{buildroot}%{_localstatedir}/www/html/itsm-ng
cp -ar . %{buildroot}%{_localstatedir}/www/html/itsm-ng

%post

setsebool -P httpd_unified 1
setsebool -P httpd_can_network_connect 1
setsebool -P httpd_can_sendmail 1
setsebool -P httpd_can_network_connect_db 1

systemctl start mariadb.service

if mysqlshow itsmng ; then
    echo "Nothing to update"
else 
    mysql --execute="CREATE DATABASE itsmng; CREATE USER 'itsmng'@'localhost' IDENTIFIED BY 'itsmng'; GRANT ALL PRIVILEGES ON itsmng.* TO itsmng@localhost; FLUSH PRIVILEGES;"
fi

chown -R apache: /var/www/html/itsm-ng

systemctl restart httpd

%postun

rm -rf /var/www/html/itsm-ng/config /var/www/html/itsm-ng/files
systemctl restart httpd

%clean
rm -rf $RPM_BUILD_ROOT

%files
/var/www/html/itsm-ng
%defattr(-, apache, apache, -)

%changelog
* Thu Aug 18 2022 Esteban Hulin <devteam@itsm-ng.com> - 1.2.0-1
- 1.2.0 Version with php 8.X compatibility fixes
* Wed Jul 27 2022 Esteban Hulin <esteban.hulin@itsm-ng.com> - 1.1.0-1
- First version being packaged