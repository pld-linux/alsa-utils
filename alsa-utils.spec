Summary:	Advanced Linux Sound Architecture (ALSA) - Utils
Summary(es):	Utilitarios para ALSA (Advanced Linux Sound Architecture)
Summary(pl):	Advanced Linux Sound Architecture (ALSA) - Narzêdzia
Summary(pt_BR):	Utilitários para o ALSA (Advanced Linux Sound Architecture)
Name:		alsa-utils
Version:	0.5.10
Release:	5
License:	GPL
Group:		Applications/Sound
Group(de):	Applikationen/Laut
Group(es):	Aplicaciones/Sonido
Group(pl):	Aplikacje/D¼wiêk
Group(pt_BR):	Aplicações/Som
Source0:	ftp://ftp.alsa-project.org/pub/utils/%{name}-%{version}.tar.bz2
Source1:	alsasound
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-LDFLAGS.patch
URL:		http://www.alsa-project.org/
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	alsa-lib-devel >= 0.5.10
Prereq:		/sbin/depmod
Prereq:		/sbin/ldconfig
Prereq:		/sbin/chkconfig
ExcludeArch:	sparc
ExcludeArch:	sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
Advanced Linux Sound Architecture (ALSA) - Utils alsamixer, amixer,
aplay, arecord.

%description -l es
Utilitarios para el sistema ALSA, la arquitetura avanzada de sonido
para Linux.

%description -l pl
Advanced Linux Sound Architecture (ALSA) - Narzêdzia alsamixer,
amixer, aplay, arecord.

%description -l pt_BR
Utilitários para o ALSA, a arquitetura de som avançada para o Linux.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
rm -f missing
aclocal
autoconf
automake -a -c
CFLAGS="%{rpmcflags} -I/usr/include/ncurses"
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions"
%configure

%{__make} 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/alsasound

rm -f $RPM_BUILD_ROOT%{_mandir}/man1/arecord.1
echo ".so aplay.1" > $RPM_BUILD_ROOT%{_mandir}/man1/arecord.1

touch $RPM_BUILD_ROOT%{_sysconfdir}/asound.conf

gzip -9nf README ChangeLog

%post
/sbin/chkconfig --add alsasound
if [ -f /var/lock/subsys/alsasound ]; then
	/etc/rc.d/init.d/alsasound restart >&2
else
	echo "Run \"/etc/rc.d/init.d/alsasound start\" to start ALSA %{version} services."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/alsasound ]; then
		/etc/rc.d/init.d/alsasound stop >&2
	fi
	/sbin/chkconfig --del alsasound
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/asound.conf
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*

%{_mandir}/man1/alsactl.1*
%{_mandir}/man1/alsamixer.1*
%{_mandir}/man1/amixer.1*
%{_mandir}/man1/aplay.1*
%{_mandir}/man1/arecord.1*
