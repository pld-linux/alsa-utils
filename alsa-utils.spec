Summary:	Advanced Linux Sound Architecture (ALSA) - Utils
Summary(pl):	Advanced Linux Sound Architecture (ALSA) - Narzêdzia
Name:		alsa-utils
Version:	0.5.5
Release:	1
License:	GPL
Group:		Applications/Sound
Group(pl):	Aplikacje/D¼wiêk
Source0:	ftp://ftp.alsa-project.org/pub/utils/alsa-utils-%{version}.tar.bz2
Source1:	alsasound
Patch0:		alsa-utils-DESTDIR.patch
URL:		http://www.alsa-project.org/
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	libtool
BuildConflicts:	alsa-lib <= 0.4.0
Prereq:		/sbin/depmod
Prereq:		/sbin/ldconfig
Prereq:		/sbin/chkconfig
ExcludeArch:	sparc
ExcludeArch:	sparc64
BuildRoot:	/tmp/%{name}-%{version}-root

%define		_sysconfdir	/etc
%define		_kernel_ver	%(grep UTS_RELEASE /usr/src/linux/include/linux/version.h 2>/dev/null | cut -d'"' -f2)

%description
Advanced Linux Sound Architecture (ALSA) - Utils alsamixer, amixer, aplay,
arecord.

%description -l pl
Advanced Linux Sound Architecture (ALSA) - Narzêdzia alsamixer, amixer,
aplay, arecord.

%prep
%setup -q
%patch0 -p2

%build
LDFLAGS="-s"; export LDFLAGS
cp aclocal.m4 acinclude.m4
aclocal
automake -c || :
autoconf
CPPFLAGS="-I/usr/include/ncurses" ; export CPPFLAGS
CFLAGS="$RPM_OPT_FLAGS"; export CFLAGS
CXXFLAGS="$RPM_OPT_FLAGS -fno-rtti -fno-exceptions" ; export CXXFLAGS
%configure

make 


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,/etc/rc.d/init.d}

make install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/alsasound

touch $RPM_BUILD_ROOT/etc/asound.conf

#mv $RPM_BUILD_ROOT/usr/etc/xamixer.conf $RPM_BUILD_ROOT/etc

gzip -9nf README ChangeLog \
	$RPM_BUILD_ROOT%{_mandir}/man1/*

%post
/sbin/chkconfig --add alsasound
if test -r /var/lock/subsys/alsasound; then
	/etc/rc.d/init.d/alsasound restart >&2
else
	echo "Run \"/etc/rc.d/init.d/alsasound start\" to start ALSA %{version} services."
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
%config(noreplace) %verify(not md5 size mtime) /etc/asound.conf
#%config(noreplace) %verify(not md5 size mtime) /etc/xamixer.conf

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*

%attr(754,root,root) /etc/rc.d/init.d/*

%{_mandir}/man1/alsactl.1*
%{_mandir}/man1/alsamixer.1*
%{_mandir}/man1/amixer.1*
%{_mandir}/man1/aplay.1*
%{_mandir}/man1/arecord.1*
