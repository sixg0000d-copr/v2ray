# Generated by go2rpm 1.3

# https://github.com/v2fly/v2ray-core
%global goipath         github.com/v2fly/v2ray-core/v4
Version:                4.38.3

%gometa

%global golicenses      LICENSE
%global godocs          README.md SECURITY.md

Name:                   v2ray-core
Release:                3%{?dist}
Summary:                A platform for building proxies to bypass network restrictions
License:                MIT
URL:                    https://www.v2fly.org/

%global common_description %{expand:
Project V is a set of network tools that help you to build your own computer
network. It secures your network connections and thus protects your privacy.
For more details please see %{url}}

# Source0 & Source1 is created by:
# spectool -g -s 0 v2ray-core.spec
# tar xzf %%{archivename}.tar.gz
# cd %%{archivename}
# go mod vendor
# tar czf ../%%{archivename}-vendor.tar.gz vendor
Source0:                %{gosource}
Source1:                %{archivename}-vendor.tar.gz
Source10:               v2ray.service
Source11:               v2ray@.service
Source12:               v2ray-confdir.service
Source20:               null.json
Source21:               00_log.json
Source22:               03_routing.json
Source23:               06_outbounds.json

BuildRequires:          systemd-rpm-macros

%{?systemd_requires}
Requires:               systemd >= 232
Recommends:             %{_datadir}/v2ray/geoip.dat
Recommends:             %{_datadir}/v2ray/geosite.dat

Provides:               v2ray = %{version}-%{release}
Obsoletes:              v2ray < 4.32.1-2

%package -n v2ray-confdir
Summary:                Enable multiple config for v2ray
%{?systemd_requires}
Requires:               systemd >= 232
Requires:               %{name}%{?_isa} = %{version}-%{release}

%package -n v2ray-extra
Summary:                Browser forwarder asset for v2ray
Requires:               %{name}%{?_isa} = %{version}-%{release}

%description
%{common_description}


%description -n v2ray-confdir
Enable multiple config for v2ray.


%description -n v2ray-extra
Browser forwarder:
Use browser's WebSocket framework to automatically relay v2ray traffic,
which will have the same TLS fingerprint as browser initialized WSS traffic.
There are v2ray browser forwarder asset files.


%prep
%if 0%{?fedora}
%goprep -k
%else
%forgesetup
%global gobuilddir  %{_builddir}/%{archivename}/_build
if [[ ! -e "%{gobuilddir}/bin" ]] ; then
    install -m 0755 -vd %{gobuilddir}/bin
    export GOPATH="%{gobuilddir}"
fi
%global gosourcedir %{gobuilddir}/src/%{goipath}
if [[ ! -e "%{gosourcedir}" ]] ; then
    install -m 0755 -vd $(dirname %{gosourcedir})
    ln -fs %{_builddir}/%{archivename} %{gosourcedir}
fi
cd %{gosourcedir}
%endif
%global v2ray_asset %{gosourcedir}/release

# go vendor
%setup -qTD -a 1 %{forgesetupargs}


%build
# build: binaries
export LDFLAGS="-linkmode=external "
%gobuild -o %{gobuilddir}/bin/v2ray %{goipath}/main
unset LDFLAGS

%if 0%{?fedora}
export LDFLAGS="-linkmode=external " BUILDTAGS="confonly"
%gobuild -o %{gobuilddir}/bin/v2ctl %{goipath}/infra/control/main
unset LDFLAGS BUILDTAGS
%else
go build \
    -buildmode pie \
    -compiler gc \
    -tags="rpm_crashtraceback confonly" \
    -ldflags="-linkmode=external -X %{goipath}/version=%{version} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" \
    -trimpath \
    -a -v \
    -o %{gobuilddir}/bin/v2ctl \
    %{goipath}/infra/control/main
%endif


%install
# install: binaries
install -m 0755 -vd                                                   %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/v2ray                           %{buildroot}%{_bindir}/v2ray
install -m 0755 -vp %{gobuilddir}/bin/v2ctl                           %{buildroot}%{_bindir}/v2ctl
# install: config
install -m 0755 -vd                                                   %{buildroot}%{_sysconfdir}/v2ray
install -m 0644 -vp %{v2ray_asset}/config/config.json                 %{buildroot}%{_sysconfdir}/v2ray/config.json
# install: v2ray-confdir configs
install -m 0755 -vd                                                   %{buildroot}%{_sysconfdir}/v2ray.confdir
install -m 0644 -vp %{S:21}                                           %{buildroot}%{_sysconfdir}/v2ray.confdir/00_log.json
install -m 0644 -vp %{S:20}                                           %{buildroot}%{_sysconfdir}/v2ray.confdir/01_api.json
install -m 0644 -vp %{S:20}                                           %{buildroot}%{_sysconfdir}/v2ray.confdir/02_dns.json
install -m 0644 -vp %{S:22}                                           %{buildroot}%{_sysconfdir}/v2ray.confdir/03_routing.json
install -m 0644 -vp %{S:20}                                           %{buildroot}%{_sysconfdir}/v2ray.confdir/04_policy.json
install -m 0644 -vp %{S:20}                                           %{buildroot}%{_sysconfdir}/v2ray.confdir/05_inbounds.json
install -m 0644 -vp %{S:23}                                           %{buildroot}%{_sysconfdir}/v2ray.confdir/06_outbounds.json
install -m 0644 -vp %{S:20}                                           %{buildroot}%{_sysconfdir}/v2ray.confdir/07_transport.json
install -m 0644 -vp %{S:20}                                           %{buildroot}%{_sysconfdir}/v2ray.confdir/08_stats.json
install -m 0644 -vp %{S:20}                                           %{buildroot}%{_sysconfdir}/v2ray.confdir/09_reverse.json
install -m 0644 -vp %{S:20}                                           %{buildroot}%{_sysconfdir}/v2ray.confdir/10_fakedns.json
install -m 0644 -vp %{S:20}                                           %{buildroot}%{_sysconfdir}/v2ray.confdir/11_browserForwarder.json
install -m 0644 -vp %{S:20}                                           %{buildroot}%{_sysconfdir}/v2ray.confdir/12_observatory.json
# install: systemd
install -m 0755 -vd                                                   %{buildroot}%{_unitdir}
install -m 0644 -vp %{S:10}                                           %{buildroot}%{_unitdir}/v2ray.service
install -m 0644 -vp %{S:11}                                           %{buildroot}%{_unitdir}/v2ray@.service
install -m 0644 -vp %{S:12}                                           %{buildroot}%{_unitdir}/v2ray-confdir.service
# install: v2ray assets directory
install -m 0755 -vd                                                   %{buildroot}%{_datadir}/v2ray
# install: v2ray extra
install -m 0755 -vd                                                   %{buildroot}%{_datadir}/v2ray/browserforwarder
install -m 0644 -vp %{v2ray_asset}/extra/browserforwarder/index.html  %{buildroot}%{_datadir}/v2ray/browserforwarder/index.html
install -m 0644 -vp %{v2ray_asset}/extra/browserforwarder/index.js    %{buildroot}%{_datadir}/v2ray/browserforwarder/index.js


%post
%systemd_post v2ray.service v2ray@.service

%preun
# See https://github.com/systemd/systemd/issues/15620
INSTANCES=$(/usr/bin/systemctl list-units --type=service --state=active --no-legend --no-pager 'v2ray*' | /usr/bin/awk '{print $1}')
%systemd_preun $INSTANCES

%postun
# See https://github.com/systemd/systemd/issues/15620
INSTANCES=$(/usr/bin/systemctl list-units --type=service --state=active --no-legend --no-pager 'v2ray*' | /usr/bin/awk '{print $1}')
%systemd_postun_with_restart $INSTANCES

%post -n v2ray-confdir
%systemd_post v2ray-confdir.service

%preun -n v2ray-confdir
%systemd_preun v2ray-confdir.service

%postun -n v2ray-confdir
%systemd_postun_with_restart v2ray-confdir.service


%files
%license %{golicenses}
%doc %{godocs}
# binaries
%{_bindir}/v2ray
%{_bindir}/v2ctl
# config
%dir %{_sysconfdir}/v2ray
%config(noreplace) %{_sysconfdir}/v2ray/config.json
# systemd
%{_unitdir}/v2ray.service
%{_unitdir}/v2ray@.service
# v2ray assets directory
%dir %{_datadir}/v2ray


%files -n v2ray-confdir
# config
%dir %{_sysconfdir}/v2ray.confdir
%config(noreplace) %{_sysconfdir}/v2ray.confdir/00_log.json
%config(noreplace) %{_sysconfdir}/v2ray.confdir/01_api.json
%config(noreplace) %{_sysconfdir}/v2ray.confdir/02_dns.json
%config(noreplace) %{_sysconfdir}/v2ray.confdir/03_routing.json
%config(noreplace) %{_sysconfdir}/v2ray.confdir/04_policy.json
%config(noreplace) %{_sysconfdir}/v2ray.confdir/05_inbounds.json
%config(noreplace) %{_sysconfdir}/v2ray.confdir/06_outbounds.json
%config(noreplace) %{_sysconfdir}/v2ray.confdir/07_transport.json
%config(noreplace) %{_sysconfdir}/v2ray.confdir/08_stats.json
%config(noreplace) %{_sysconfdir}/v2ray.confdir/09_reverse.json
%config(noreplace) %{_sysconfdir}/v2ray.confdir/10_fakedns.json
%config(noreplace) %{_sysconfdir}/v2ray.confdir/11_browserForwarder.json
%config(noreplace) %{_sysconfdir}/v2ray.confdir/12_observatory.json
# systemd
%{_unitdir}/v2ray-confdir.service


%files -n v2ray-extra
%dir %{_datadir}/v2ray/browserforwarder
%{_datadir}/v2ray/browserforwarder/index.html
%{_datadir}/v2ray/browserforwarder/index.js


%changelog
* Thu May 06 2021 sixg0000d <sixg0000d@gmail.com> - 4.38.3-3
- Add v2ray-extra

* Sun May 02 2021 sixg0000d <sixg0000d@gmail.com> - 4.38.3-2
- Update scirptlets

* Sat May 01 2021 sixg0000d <sixg0000d@gmail.com> - 4.38.3-1
- Update to 4.38.3

* Fri Apr 30 2021 sixg0000d <sixg0000d@gmail.com> - 4.38.2-1
- Update to 4.38.2

* Mon Apr 26 2021 sixg0000d <sixg0000d@gmail.com> - 4.38.1-1
- Update to 4.38.1

* Sat Apr 24 2021 sixg0000d <sixg0000d@gmail.com> - 4.38.0-3.20210422gita21e4a7
- Add 12_observatory.json for v2ray-confdir

* Thu Apr 22 2021 sixg0000d <sixg0000d@gmail.com> - 4.38.0-2.20210422gita21e4a7
- Update to 4.38.0-2.20210422gita21e4a7

* Mon Apr 19 2021 sixg0000d <sixg0000d@gmail.com> - 4.38.0-2
- Patch: fixed a panic issue

* Sat Apr 17 2021 sixg0000d <sixg0000d@gmail.com> - 4.38.0-1
- Update to 4.38.0

* Fri Apr 16 2021 sixg0000d <sixg0000d@gmail.com> - 4.37.3-1
- Initial v2ray-core
