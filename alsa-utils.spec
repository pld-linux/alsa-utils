%define         ver      0.3.0
%define         patchlvl pre3

Summary:	Advanced Linux Sound Architecture (ALSA) - Utils
Summary(pl):	Advanced Linux Sound Architecture (ALSA) - Narzêdzia
Name:		alsa-utils
Version:	%{ver}%{patchlvl}
Release:	3
Copyright:	GPL
Group:		Applications/Sound
Group(pl):	Aplikacje/D¼wiêk
Source0:	ftp://alsa.jcu.cz/pub/utils/%{name}-%{ver}-%{patchlvl}.tar.gz 
Source1:	alsasound
Patch0:		alsa-utils-DESTDIR.patch
Patch1:		alsa-utils-opt.patch
BuildPrereq:	alsa-driver-devel
BuildPrereq:	alsa-lib-devel
BuildPrereq:	libstdc++-devel
BuildPrereq:	ncurses-devel
Requires:	alsa-driver
Prereq:		/sbin/chkconfig
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Advanced Linux Sound Architecture (ALSA) - Utils
alsamixer, amixer, aplay, arecord

%description -l pl
Advanced Linux Sound Architecture (ALSA) - Narzêdzia
alsamixer, amixer, aplay, arecord

%prep
%setup  -q -n %{name}-%{ver}-%{patchlvl}
%patch0 -p0
%patch1 -p1

%build
./configure %{_target_platform} \
	--prefix=%{_prefix} \
	--mandir=%{_mandir}

make OPT="$RPM_OPT_FLAGS -I/usr/include/ncurses"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,/etc/rc.d/init.d}

make install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/alsasound

touch $RPM_BUILD_ROOT/etc/asound.conf


gzip -9nf README ChangeLog amixer/README.first \
	$RPM_BUILD_ROOT%{_mandir}/man1/*

%post
/sbin/chkconfig --add alsasound
if test -r /var/run/alsasound.pid; then
	/etc/rc.d/init.d/alsasound stop >&2
	/etc/rc.d/init.d/alsasound start >&2
else
	echo "Run \"/etc/rc.d/init.d/alsasound start\" to start alsasound daemon."
fi

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del alsasound
	/etc/rc.d/init.d/alsasound stop >&2
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,ChangeLog,amixer/README.first}.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*

%{_mandir}/man1/*

%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) %config /etc/asound.conf

%changelog
* Tue May 25 1999 Piotr Czerwiñski <pius@pld.org.pl> 
  [0.3.0pre3-3]
- package is FHS 2.0 compliant,
- based on spec file made by Helge Jensen <slog@slog.dk>,
- rewritten for PLD use by me and Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>,
- pl translation by Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>.
