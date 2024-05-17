%global useselinux 1

Name:           itsm-ng
Version:        1.6.3
Release:        1%{?dist}
Summary:        IT Equipment Manager
Summary(fr):    Gestion Libre de Parc Informatique

Group:          Applications/Internet
License:        GPLv2
URL:            http://www.itsm-ng.org/
Source0:        https://github.com/itsmng/itsm-ng/releases/download/v%{version}/%{name}-%{version}.tgz
Source1:        itsm-ng.conf
Source2:        downstream.php
Source3:        local_define.php

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       httpd
Requires:       mariadb-server
Requires:       php >= 7.4
Requires:		php-bcmath
Requires:       php-ctype
Requires:       php-curl
Requires:       php-gd
Requires:       php-iconv
Requires:       php-intl
Requires:       php-json
Requires:       php-mbstring
Requires:       php-simplexml
Requires:       php-ldap
Requires:       php-opcache
Recommends:     php-sodium

%if 0%{?suse_version}
Requires:		apache2-mod_php81
Requires:		php81-APCu
Requires:		php-fileinfo
Requires:		php-zlib
Recommends:     php-exif
%else
Requires:       php-pecl-apcu
Recommends:     php-selinux
%endif

%if 0%{?rhel} || 0%{?fedora}
Requires:		crontabs
Requires:		php-mysqli
%else
Requires:		php-mysql
%endif

%undefine __brp_mangle_shebangs

%description
ITSM-NG application RPM package

%prep
%setup -q -n %{name}


%install
# Copy local_define in config folder
mkdir -p %{buildroot}%{_sysconfdir}/itsm-ng
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/itsm-ng

# Copy ITSM-NG app 
mkdir -p %{buildroot}%{_datadir}/itsm-ng
cp -ar . %{buildroot}%{_datadir}/itsm-ng

# Copy downstream.php to ITSM-NG inc folder
mkdir -p %{buildroot}%{_datadir}/itsm-ng/inc
cp %{SOURCE2} %{buildroot}%{_datadir}/itsm-ng/inc

# Copy ITSM-NG files folder
mkdir -p %{buildroot}%{_sharedstatedir}/itsm-ng
cp -ar %{buildroot}%{_datadir}/itsm-ng/files/* %{buildroot}%{_sharedstatedir}/itsm-ng

# Create ITSM-NG apache configuration folder
%if 0%{?rhel} || 0%{?fedora}
        mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
	cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/itsm-ng.conf
%else
        mkdir -p %{buildroot}%{_sysconfdir}/apache2/conf.d
        cp %{SOURCE1} %{buildroot}/%{_sysconfdir}/apache2/conf.d/itsm-ng.conf
%endif

%post
%if %{useselinux}
(
setsebool -P httpd_unified 1
setsebool -P httpd_can_network_connect 1
setsebool -P httpd_can_sendmail 1
setsebool -P httpd_can_network_connect_db 1	

chcon -R -t httpd_sys_rw_content_t %{_sysconfdir}/itsm-ng/

if [ -f /etc/redhat-release ]; then
	setfacl -m g:apache:rwx /var/lib/itsm-ng/
else
	setfacl -m g:wwwrun:rwx /var/lib/itsm-ng/
fi
) &>/dev/null
%endif

%{_bindir}/systemctl condrestart httpd > /dev/null 2>&1 || :

%postun
%{_bindir}/systemctl condrestart httpd > /dev/null 2>&1 || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%if 0%{?rhel} || 0%{?fedora}
	%config(noreplace,missingok) %attr(750,apache,apache) %{_sysconfdir}/itsm-ng
	%config(noreplace) %{_sysconfdir}/httpd/conf.d/itsm-ng.conf
	%attr(750,apache,apache) %{_datadir}/itsm-ng
	%attr(750,apache,apache) %{_sharedstatedir}/itsm-ng
%else
	%config(noreplace,missingok) %attr(750,wwwrun,www) %{_sysconfdir}/itsm-ng
    %config(noreplace) %{_sysconfdir}/apache2/conf.d/itsm-ng.conf
	%attr(750,wwwrun,www) %{_datadir}/itsm-ng
    %attr(750,wwwrun,www) %{_sharedstatedir}/itsm-ng
%endif

%changelog
* Tue Oct 24 2023 Florian Blanchet <florian.blanchet@itsm-ng.com> - 1.5.1-1
- Refactor .SPEC file

* Fri Dec 09 2022 ITSM Dev Team <devteam@itsm-ng.com> - 1.3.0-2
- Move config files to /etc/itsm-ng
- Move files to /var/lib/itsm-ng
- Move itsm-ng app to /usr/share/itsm-ng
- Add itsm-ng apache configuration file 
- Add preinstallation script to save old ITSM-NG folder before upgrade
- Restore files, config, plugins and itsm-ng apache config file after upgrade
- Rename config_db.php to config_db.php.old

* Wed Nov 16 2022 ITSM Dev Team <devteam@itsm-ng.com> - 1.3.0-1
- Update to 1.3.0

* Thu Aug 18 2022 Esteban Hulin <devteam@itsm-ng.com> - 1.2.0-1
- 1.2.0 Version with php 8.X compatibility fixes

* Wed Jul 27 2022 Esteban Hulin <esteban.hulin@itsm-ng.com> - 1.1.0-1
- First version being packaged
