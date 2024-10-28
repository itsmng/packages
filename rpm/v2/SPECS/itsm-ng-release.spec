Name:			itsm-ng-release
Version:		1.0
Release:		1%{?dist}
Summary:		ITSM-NG YUM configuration repository
Summary(fr):	Configuration de YUM pour le dépôt ITSM-NG

License:		GPL-2.0-only
URL:			http://www.itsm-ng.org/
# RHEL repo
Source0:		https://rpm.itsm-ng.org/itsm-ng.repo
# Fedora repo
Source1:		https://rpm.itsm-ng.org/itsm-ng-fedora.repo
BuildArch:		noarch

%description
This package contains yum configuration for the ITSM-NG RPM repository.

%prep
%setup -c -T

%build
# nothing to do

%install
# Install yum configuration

# RHEL
%if 0%{?rhel}
mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d
cp %{SOURCE0} %{buildroot}%{_sysconfdir}/yum.repos.d/itsm-ng.repo
%endif

# Fedora
%if 0%{?fedora}
mkdir -p %{buildroot}%{_sysconfdir}/yum.repos.d
cp %{SOURCE1} %{buildroot}%{_sysconfdir}/yum.repos.d/itsm-ng.repo
%endif


%files
%{_sysconfdir}/yum.repos.d/itsm-ng.repo

%changelog
* Wed Aug 07 2024 Florian Blanchet <florian.blanchet@itsm-ng.com> - 1.0-1
- Initial release for RHEL and Fedora
