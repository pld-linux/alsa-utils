Summary:	Advanced Linux Sound Architecture (ALSA) - Utils
Summary(pl):	Advanced Linux Sound Architecture (ALSA) - Narzêdzia
Name:		alsa-utils
Version:	0.3.1
Release:	1
Copyright:	GPL
Group:		Applications/Sound
Group(pl):	Aplikacje/D¼wiêk
Source0:	ftp://ftp.alsa-project.org/pub/utils/%{name}-%{version}.tar.gz 
Source1:	alsasound
Patch0:		alsa-utils-DESTDIR.patch
Patch1:		alsa-utils-xamixer.patch
BuildPrereq:	alsa-driver-devel
BuildPrereq:	alsa-lib-devel
BuildPrereq:	libstdc++-devel
BuildPrereq:	ncurses-devel
BuildPrereq:	gtk+-devel
BuildPrereq:	XFree86-libs
BuildPrereq:	glib-devel
Requires:	alsa-driver
Prereq:		/sbin/chkconfig
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Advanced Linux Sound Architecture (ALSA) - Utils alsamixer, amixer, aplay,
arecord.

%description -l pl
Advanced Linux Sound Architecture (ALSA) - Narzêdzia alsamixer, amixer,
aplay, arecord.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1

%build
autoconf
CFLAGS="$RPM_OPT_FLAGS -I/usr/include/ncurses" LDFLAGS="-s" \
CXXFLAGS="$RPM_OPT_FLAGS -fno-rtti -fno-exceptions" \
./configure %{_target_platform} \
	--prefix=%{_prefix}

make 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,/etc/rc.d/init.d}

make install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/alsasound

touch $RPM_BUILD_ROOT/etc/asound.conf

rm -f $RPM_BUILD_ROOT%{_mandir}/man1/arecord.1
echo ".so aplay.1" > $RPM_BUILD_ROOT%{_mandir}/man1/arecord.1
mv $RPM_BUILD_ROOT/usr/etc/xamixer.conf $RPM_BUILD_ROOT/etc

gzip -9nf README ChangeLog \
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
%doc {README,ChangeLog}.gz
%config(noreplace) /etc/asound.conf
%config(noreplace) /etc/xamixer.conf
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*

%{_mandir}/man1/*

%attr(754,root,root) /etc/rc.d/init.d/*
