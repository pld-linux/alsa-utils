Summary:	Advanced Linux Sound Architecture (ALSA) - Utils
Summary(es):	Utilitarios para ALSA (Advanced Linux Sound Architecture)
Summary(pl):	Advanced Linux Sound Architecture (ALSA) - NarzЙdzia
Summary(pt_BR):	UtilitАrios para o ALSA (Advanced Linux Sound Architecture)
Summary(ru):	Утилиты командной строки для ALSA project
Summary(uk):	Утил╕ти командного рядка для ALSA project
Name:		alsa-utils
Version:	0.9.0rc1
Release:	1
License:	GPL
Group:		Applications/Sound
Source0:	ftp://ftp.alsa-project.org/pub/utils/%{name}-%{version}.tar.bz2
Source1:	alsasound
Source2:	alsa-oss-pcm
#Patch0:		%{name}-DESTDIR.patch
#Patch1:		%{name}-LDFLAGS.patch
URL:		http://www.alsa-project.org/
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	alsa-lib-devel >= 0.9.0rc1
Prereq:		awk
Prereq:		/sbin/depmod
Prereq:		/sbin/ldconfig
Prereq:		/sbin/chkconfig
ExcludeArch:	sparc
ExcludeArch:	sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc

%description
This packages contains command line utilities for the ALSA project:

 - alsactl       - utility for store / restore of soundcard settings
 - aplay/arecord - utility for playback / record of .wav, .voc, .au files
 - amixer        - a command line mixer
 - alsamixer     - ncurses mixer


%description -l es
Utilitarios para el sistema ALSA, la arquitetura avanzada de sonido
para Linux.


%description -l pl
Pakiet zawiera nastЙpuj╠ce, dziaЁaj╠ce z linii poleceЯ, narzЙdzia dla
projektu ALSA (Advanced Linux Sound Architecture):

 - alsactl       - narzЙdzie do zapamiЙtywania / przywracania ustawieЯ
                   karty sieciowej
 - aplay/arecord - narzЙdzia do odtwarzania / nagrywania plikСw .wav,
                   .voc, .au
 - amixer        - mikser dziaЁaj╠cy z linii poleceЯ
 - alsamixer     - mikser z interfejsem opartym o ncurses


%description -l pt_BR
UtilitАrios para o ALSA, a arquitetura de som avanГada para o Linux.


%description -l ru
Этот пакет содержит утилиты командной строки для ALSA project:

 - alsactl       - утилита для сохранения/восстановления настроек
                   звуковой карты
 - aplay/arecord - утилита для записи/проигрывания файлов .wav, .voc,
                   .au
 - amixer        - микшер, управляемый из командной строки
 - alsamixer     - микшер с интерфейсом ncurses


%description -l uk
Цей пакет м╕стить утил╕ти командного рядка для ALSA project:

 - alsactl       - утил╕та для збереження/в╕дновлення настанов
                   звуково╖ карти
 - aplay/arecord - утил╕та для запису/програвання файл╕в .wav, .voc,
                   .au
 - amixer        - м╕кшер, який керу╓ться з командного рядка
 - alsamixer     - м╕кшер з ╕нтерфейсом ncurses


%prep
%setup -q
#%patch0 -p1
#%patch1 -p1

%build
rm -f missing
aclocal
autoconf
automake -a -c -f
CFLAGS="%{rpmcflags} -I/usr/include/ncurses"
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions"
%configure

%{__make} 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/alsasound
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig

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
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*

%{_mandir}/man1/aconnect.1*
%{_mandir}/man1/alsactl.1*
%{_mandir}/man1/alsamixer.1*
%{_mandir}/man1/amixer.1*
%{_mandir}/man1/aplay.1*
%{_mandir}/man1/arecord.1*
%{_mandir}/man1/aseqnet.1*
