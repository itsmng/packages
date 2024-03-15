%global useselinux 1

%global tarname itsm-ng
%global official_version 2.0.0~rc2

%undefine _disable_source_fetch

Name:           itsm-ng
Version:        2.0.0_rc2
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
Requires:       php(httpd)
Requires:       php >= 8.1
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
Requires:       php-pecl-apcu
Requires:       php-opcache

Requires(postun): %{_bindir}/systemctl
Requires(post):   %{_bindir}/systemctl
%if %{useselinux}
Requires(post):   /sbin/restorecon
Requires(post):   /usr/sbin/semanage
Requires(postun): /usr/sbin/semanage
%endif
Requires:         crontabs

Recommends:	php-sodium
Recommends:	php-selinux

%undefine __brp_mangle_shebangs

%description
ITSM-NG application RPM package

%prep
%setup -q -n %{name}

%pre
# Backup old ITSM-NG app if exists
if [ -d "%{_localstatedir}/www/html/itsm-ng/config" ]
then
    # Create backup folder
    mkdir -p %{_sharedstatedir}/itsmbackup_update/files
    # Copy files to save
    cp -ar %{_localstatedir}/www/html/itsm-ng/files/* %{_sharedstatedir}/itsmbackup_update/files
    cp -ar %{_localstatedir}/www/html/itsm-ng/plugins %{_sharedstatedir}/itsmbackup_update
fi


##########################################
#                                        #
#                Install                 #
#                                        #
##########################################
%install
# Create ITSM-NG app folder
mkdir -p %{buildroot}%{_datadir}/itsm-ng
# Create ITSM-NG config folder
mkdir -p %{buildroot}%{_sysconfdir}/itsm-ng
# Create ITSM-NG files folder
mkdir -p %{buildroot}%{_sharedstatedir}/itsm-ng
# Create ITSM-NG apache configuration folder
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d

# Copy local_define in config folder
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/itsm-ng
# Copy ITSM-NG app 
cp -ar . %{buildroot}%{_datadir}/itsm-ng
# Copy downstream.php to ITSM-NG inc folder
cp %{SOURCE2} %{buildroot}%{_datadir}/itsm-ng/inc
# Copy ITSM-NG files folder
cp -ar %{buildroot}%{_datadir}/itsm-ng/files/* %{buildroot}%{_sharedstatedir}/itsm-ng
# Copy ITSM-NG apache configuration file
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d

##########################################
#                                        #
#              Postinstall               #
#                                        #
##########################################
%post
# Restore backup if exists
if [ -d %{_sharedstatedir}/itsmbackup_update ]
then
    # Restore files and folders
    cp -ar %{_sharedstatedir}/itsmbackup_update/files/* %{_sharedstatedir}/itsm-ng
    cp -ar %{_sharedstatedir}/itsmbackup_update/plugins/* %{_datadir}/itsm-ng/plugins

    # Remove backup folder
    rm -rf %{_sharedstatedir}/itsmbackup_update
fi

install -Dpm 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/httpd/conf.d/itsm-ng.conf
 
%if %{useselinux}
(
setsebool -P httpd_unified 1
setsebool -P httpd_can_network_connect 1
setsebool -P httpd_can_sendmail 1
setsebool -P httpd_can_network_connect_db 1	
) &>/dev/null
%endif

# Set apache rights
chown -R apache: %{_sysconfdir}/itsm-ng
chown -R apache: %{_sharedstatedir}/itsm-ng
chown -R apache: %{_datadir}/itsm-ng

%{_bindir}/systemctl condrestart httpd > /dev/null 2>&1 || :

##########################################
#                                        #
#             Postuninstall              #
#                                        #
##########################################
%postun
if [ -d %{_localstatedir}/www/html/itsm-ng/config ]
then
    rm -rf %{_localstatedir}/www/html/itsm-ng/config
fi
if [ -d %{_localstatedir}/www/html/itsm-ng/files ]
then
    rm -rf %{_localstatedir}/www/html/itsm-ng/files
fi

%{_bindir}/systemctl condrestart httpd > /dev/null 2>&1 || :

##########################################
#                                        #
#                 Clean                  #
#                                        #
##########################################
%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_datadir}/itsm-ng
%defattr(755, apache, apache, -)
%{_sharedstatedir}/itsm-ng
%defattr(755, apache, apache, -)

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
