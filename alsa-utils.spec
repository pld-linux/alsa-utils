Summary:	Advanced Linux Sound Architecture (ALSA) - Utils
Summary(es):	Utilitarios para ALSA (Advanced Linux Sound Architecture)
Summary(pl):	Advanced Linux Sound Architecture (ALSA) - Narzêdzia
Summary(pt_BR):	Utilitários para o ALSA (Advanced Linux Sound Architecture)
Summary(ru):	õÔÉÌÉÔÙ ËÏÍÁÎÄÎÏÊ ÓÔÒÏËÉ ÄÌÑ ALSA project
Summary(uk):	õÔÉÌ¦ÔÉ ËÏÍÁÎÄÎÏÇÏ ÒÑÄËÁ ÄÌÑ ALSA project
Name:		alsa-utils
Version:	0.5.10
Release:	7
License:	GPL
Group:		Applications/Sound
Group(cs):	Aplikace/Zvuk
Group(da):	Programmer/Lyd
Group(de):	Applikationen/Laut
Group(es):	Aplicaciones/Sonido
Group(fr):	Aplicações/Son
Group(is):	Forrit/Hljóð
Group(it):	Applicazioni/Audio
Group(no):	Applikasjoner/Lyd
Group(pl):	Aplikacje/D¼wiêk
Group(pt):	Aplicações/Som
Group(pt_BR):	Aplicações/Som
Group(ru):	ðÒÉÌÏÖÅÎÉÑ/ú×ÕË
Group(sl):	Programi/Zvok
Group(sv):	Tillämpningar/Ljud
Group(uk):	ðÒÉËÌÁÄÎ¦ ðÒÏÇÒÁÍÉ/ú×ÕË
Source0:	ftp://ftp.alsa-project.org/pub/utils/%{name}-%{version}.tar.bz2
Source1:	alsasound
Source2:	alsa-oss-pcm
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
Pakiet zawiera nastêpuj±ce, dzia³aj±ce z linii poleceñ, narzêdzia dla
projektu ALSA (Advanced Linux Sound Architecture):

 - alsactl       - narzêdzie do zapamiêtywania / przywracania ustawieñ
                   karty sieciowej
 - aplay/arecord - narzêdzia do odtwarzania / nagrywania plików .wav,
                   .voc, .au
 - amixer        - mikser dzia³aj±cy z linii poleceñ
 - alsamixer     - mikser z interfejsem opartym o ncurses


%description -l pt_BR
Utilitários para o ALSA, a arquitetura de som avançada para o Linux.


%description -l ru
üÔÏÔ ÐÁËÅÔ ÓÏÄÅÒÖÉÔ ÕÔÉÌÉÔÙ ËÏÍÁÎÄÎÏÊ ÓÔÒÏËÉ ÄÌÑ ALSA project:

 - alsactl       - ÕÔÉÌÉÔÁ ÄÌÑ ÓÏÈÒÁÎÅÎÉÑ/×ÏÓÓÔÁÎÏ×ÌÅÎÉÑ ÎÁÓÔÒÏÅË
                   Ú×ÕËÏ×ÏÊ ËÁÒÔÙ
 - aplay/arecord - ÕÔÉÌÉÔÁ ÄÌÑ ÚÁÐÉÓÉ/ÐÒÏÉÇÒÙ×ÁÎÉÑ ÆÁÊÌÏ× .wav, .voc,
                   .au
 - amixer        - ÍÉËÛÅÒ, ÕÐÒÁ×ÌÑÅÍÙÊ ÉÚ ËÏÍÁÎÄÎÏÊ ÓÔÒÏËÉ
 - alsamixer     - ÍÉËÛÅÒ Ó ÉÎÔÅÒÆÅÊÓÏÍ ncurses


%description -l uk
ãÅÊ ÐÁËÅÔ Í¦ÓÔÉÔØ ÕÔÉÌ¦ÔÉ ËÏÍÁÎÄÎÏÇÏ ÒÑÄËÁ ÄÌÑ ALSA project:

 - alsactl       - ÕÔÉÌ¦ÔÁ ÄÌÑ ÚÂÅÒÅÖÅÎÎÑ/×¦ÄÎÏ×ÌÅÎÎÑ ÎÁÓÔÁÎÏ×
                   Ú×ÕËÏ×Ï§ ËÁÒÔÉ
 - aplay/arecord - ÕÔÉÌ¦ÔÁ ÄÌÑ ÚÁÐÉÓÕ/ÐÒÏÇÒÁ×ÁÎÎÑ ÆÁÊÌ¦× .wav, .voc,
                   .au
 - amixer        - Í¦ËÛÅÒ, ÑËÉÊ ËÅÒÕ¤ÔØÓÑ Ú ËÏÍÁÎÄÎÏÇÏ ÒÑÄËÁ
 - alsamixer     - Í¦ËÛÅÒ Ú ¦ÎÔÅÒÆÅÊÓÏÍ ncurses


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

%{_mandir}/man1/alsactl.1*
%{_mandir}/man1/alsamixer.1*
%{_mandir}/man1/amixer.1*
%{_mandir}/man1/aplay.1*
%{_mandir}/man1/arecord.1*
