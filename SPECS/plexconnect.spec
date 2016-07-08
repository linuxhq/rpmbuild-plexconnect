%global date 20160428
%global commit cfd51deffb2d1159f15edc29faee56166717526c
%global short_commit %(c=%{commit}; echo ${c:0:7})

Name:		plexconnect
Version:	%{date}git%{short_commit}
Release:	1%{?dist}
Summary:	PlexConnect
Group:		System Environment/Daemons
License:	MIT
URL:		https://github.com/iBaa/PlexConnect
Source0:	https://github.com/iBaa/PlexConnect/archive/%{commit}/PlexConnect-%{commit}.tar.gz

Requires:	dnsmasq, logrotate, webserver
Requires:	python(abi) = 2.7
%if 0%{?el7}
Requires:	python-pillow
%endif
Requires(pre):	/usr/sbin/useradd
Requires(post):	chkconfig

BuildArch:	noarch
BuildRequires:	git
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source1:	%{name}.httpd
Source2:	%{name}.dnsmasq
Source3:	%{name}.nginx
Source4:	%{name}.init
Source5:	%{name}.logrotate
Source6:	%{name}.sysconfig
Source7:	%{name}.tmpfiles
Source8:	Settings.cfg
Source9:	trailers.cer
Source10:	trailers.key
Source11:	trailers.pem
Source12:	marketwatch.cer
Source13:	marketwatch.key
Source14:	marketwatch.pem

%description
PlexConnect is a clever project: a free command-line tool that 
lets you view content from your Plex Media Server on your Apple 
TV, without jailbreaking Apple's set-top box.

%prep 
%setup -q -n PlexConnect-%{commit}
%build
%install
%{__install} -m 755 -d %{buildroot}%{_localstatedir}/lib/%{name}
%{__mv} -f *.bash *.py assets %{buildroot}%{_localstatedir}/lib/%{name}
%{__install} -m 644 %{SOURCE8} %{buildroot}%{_localstatedir}/lib/%{name}

%{__install} -m 755 -d	%{buildroot}%{_sysconfdir}/dnsmasq.d \
			%{buildroot}%{_sysconfdir}/httpd/conf.d \
			%{buildroot}%{_sysconfdir}/nginx/conf.d \
			%{buildroot}%{_sysconfdir}/pki/%{name} \
			%{buildroot}%{_sysconfdir}/rc.d/init.d \
			%{buildroot}%{_sysconfdir}/sysconfig \
			%{buildroot}%{_sysconfdir}/logrotate.d \
			%{buildroot}%{_localstatedir}/{log,run}/%{name}

%{__install} -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf
%{__install} -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/dnsmasq.d/%{name}.conf
%{__install} -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/nginx/conf.d/%{name}.conf
%{__install} -m 755 %{SOURCE4} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
%{__install} -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%{__install} -m 644 %{SOURCE9} %{SOURCE10} %{SOURCE11} \
                    %{SOURCE12} %{SOURCE13} %{SOURCE14} \
                    %{buildroot}%{_sysconfdir}/pki/%{name}

%if 0%{?el7}
%{__install} -d -m 755 %{buildroot}%{_prefix}/lib/tmpfiles.d
%{__install} -m 644 %{SOURCE6} %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf
%endif

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
  useradd -r -g %{name} -s /sbin/nologin \
    -d %{_localstatedir}/lib/%{name} -c "RPM Created PlexConnectUser" %{name}

%post
/sbin/chkconfig --add %{name}

%preun
/sbin/service %{name} stop > /dev/null 2>&1
/sbin/chkconfig --del %{name}

%clean
rm -rf %{buildroot}

%files
%doc License.txt README.md support/
%defattr(-,root,root,-)
%{_sysconfdir}/rc.d/init.d/%{name}
%config(noreplace) %{_sysconfdir}/dnsmasq.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/nginx/conf.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{?el7:%{_prefix}/lib/tmpfiles.d/%{name}.conf}
%attr(-,plexconnect,plexconnect) %{_sysconfdir}/pki/%{name}/marketwatch.*
%attr(-,plexconnect,plexconnect) %{_sysconfdir}/pki/%{name}/trailers.*
%attr(-,plexconnect,plexconnect) %dir %{_localstatedir}/lib/%{name}
%attr(-,plexconnect,plexconnect) %{_localstatedir}/lib/%{name}/*
%attr(-,plexconnect,plexconnect) %dir %{_localstatedir}/log/%{name}
%attr(-,plexconnect,plexconnect) %dir %{_localstatedir}/run/%{name}

%changelog
* Thu Apr 28 2016 Taylor Kimball <taylor@linuxhq.org> - 20160428gitcfd51de-1
- Updated to commit cfd51de.
 
* Mon Jan 19 2015 Taylor Kimball <taylor@linuxhq.org> - 0.4-1
- Initial build.
