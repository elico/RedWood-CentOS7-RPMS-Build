Name:     redwood
Version:  1.1.41
Release:  1%{?dist}
Summary:  The RedWood Content-Filtering proxy
Epoch:    7
Packager: Eliezer Croitoru <ngtech1ltd@gmail.com>
Vendor:   NgTech LTD
License:  3 Clause BSD
Group:    System Environment/Daemons
URL:      https://github.com/andybalholm/redwood
Source0:  redwood.service
Source1:  redwood
Source2:  block.html
Source3:  redwood.sysconfig
Source4:  redwood.conf
Source5:  acls.conf
Source6:  pruning.conf
Source7:  safesearch.conf
Source8:  sslbumpbypass-category.conf
Source9:  sslbumpbypass.list
Source10: redwood-sslbump-init.sh
Source11: sslbump-defaultbypass-acls.conf
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(preun):  systemd
Requires(postun): systemd
Requires:       systemd-units
# Required to allow debug package auto creation
BuildRequires:  redhat-rpm-config
BuildRequires:  systemd-units

# Required to validate auto requires AutoReqProv: no
## aaaAutoReqProv: no

%description
Redwood is an internet content-filtering program. It adds flexibility and granularity to the filtering by classifying sites into multiple categories instead of just “Allow” and “Block.”

%prep

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/redwood
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/redwood/categories
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/redwood/categories/sslbumpbypass

mkdir -p ${RPM_BUILD_ROOT}/var/redwood/static
mkdir -p ${RPM_BUILD_ROOT}/var/redwood/cgi
mkdir -p ${RPM_BUILD_ROOT}/var/log/redwood
echo "#dummy" > ${RPM_BUILD_ROOT}/var/redwood/cgi/dummy.txt

install -m 644 %{SOURCE0} ${RPM_BUILD_ROOT}%{_unitdir}
install -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_sbindir}/redwood
install -m 644 %{SOURCE2} ${RPM_BUILD_ROOT}/var/redwood/static/block.html
install -m 644 %{SOURCE3} ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/redwood
install -m 644 %{SOURCE4} ${RPM_BUILD_ROOT}%{_sysconfdir}/redwood/redwood.conf
install -m 644 %{SOURCE5} ${RPM_BUILD_ROOT}%{_sysconfdir}/redwood/acls.conf
install -m 644 %{SOURCE6} ${RPM_BUILD_ROOT}%{_sysconfdir}/redwood/pruning.conf
install -m 644 %{SOURCE7} ${RPM_BUILD_ROOT}%{_sysconfdir}/redwood/safesearch.conf
install -m 644 %{SOURCE8} ${RPM_BUILD_ROOT}%{_sysconfdir}/redwood/categories/sslbumpbypass/category.conf
install -m 644 %{SOURCE9} ${RPM_BUILD_ROOT}%{_sysconfdir}/redwood/categories/sslbumpbypass/sslbumpbypass.list
install -m 644 %{SOURCE10} ${RPM_BUILD_ROOT}%{_sbindir}/redwood-sslbump-init.sh
install -m 644 %{SOURCE11} ${RPM_BUILD_ROOT}%{_sysconfdir}/redwood/sslbump-defaultbypass-acls.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%attr(755,root,root) %dir %{_sysconfdir}
%attr(755,root,root) %dir %{_sysconfdir}/sysconfig
%attr(755,root,root) %dir %{_sysconfdir}/redwood/
%attr(755,root,root) %dir %{_sysconfdir}/redwood/categories/
%attr(755,root,root) %dir %{_sysconfdir}/redwood/categories/sslbumpbypass/
%attr(755,root,root) %dir /var/redwood/cgi
%attr(755,root,root) %dir /var/log/redwood

%config(noreplace) %{_sysconfdir}/sysconfig/redwood
%config(noreplace) %{_sysconfdir}/redwood/*
%config(noreplace) /var/redwood/static/*
%config(noreplace) /var/redwood/cgi/*
%attr(755,root,root) %{_sbindir}/redwood
%attr(755,root,root) %{_sbindir}/redwood-sslbump-init.sh

%{_unitdir}/redwood.service

%post
%systemd_post redwood.service

%preun
%systemd_preun redwood.service

%postun
%systemd_postun_with_restart redwood.service

%changelog
* Thu Mar 26 2020 Eliezer Croitoru <ngtech1ltd@gmail.com>
- Release 1.1.41 Stable.
+ This version is a testing version.

