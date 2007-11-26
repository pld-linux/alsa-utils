Summary:	Advanced Linux Sound Architecture (ALSA) - Utils
Summary(es.UTF-8):	Utilitarios para ALSA (Advanced Linux Sound Architecture)
Summary(pl.UTF-8):	Advanced Linux Sound Architecture (ALSA) - Narzędzia
Summary(pt_BR.UTF-8):	Utilitários para o ALSA (Advanced Linux Sound Architecture)
Summary(ru.UTF-8):	Утилиты командной строки для ALSA project
Summary(uk.UTF-8):	Утиліти командного рядка для ALSA project
Name:		alsa-utils
Version:	1.0.14
Release:	3
License:	GPL
Group:		Applications/Sound
Source0:	ftp://ftp.alsa-project.org/pub/utils/%{name}-%{version}.tar.bz2
# Source0-md5:	6d3009c157ac6fc803696d6590a48366
Source1:	alsasound.init
Source2:	alsa-oss-pcm
URL:		http://www.alsa-project.org/
BuildRequires:	alsa-lib-devel >= 1.0.14
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	gettext-devel >= 0.14
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	alsa-lib >= 1.0.14
Requires:	awk
Requires:	dialog
Requires:	diffutils
Requires:	which
Obsoletes:	alsaconf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This packages contains command line utilities for the ALSA project:
- alsactl - utility for store / restore of soundcard settings
- aplay/arecord - utility for playback / record of .wav, .voc, .au
  files
- amixer - a command line mixer
- alsamixer - ncurses mixer

%description -l es.UTF-8
Utilitarios para el sistema ALSA, la arquitetura avanzada de sonido
para Linux.

%description -l pl.UTF-8
Pakiet zawiera następujące, działające z linii poleceń, narzędzia dla
projektu ALSA (Advanced Linux Sound Architecture):
- alsactl - narzędzie do zapamiętywania / przywracania ustawień karty
  dźwiękowej
- aplay/arecord - narzędzia do odtwarzania / nagrywania plików .wav,
  .voc, .au
- amixer - mikser działający z linii poleceń
- alsamixer - mikser z interfejsem opartym o ncurses

%description -l pt_BR.UTF-8
Utilitários para o ALSA, a arquitetura de som avançada para o Linux.

%description -l ru.UTF-8
Этот пакет содержит утилиты командной строки для ALSA project:
- alsactl - утилита для сохранения/восстановления настроек звуковой
  карты
- aplay/arecord - утилита для записи/проигрывания файлов .wav, .voc,
  .au
- amixer - микшер, управляемый из командной строки
- alsamixer - микшер с интерфейсом ncurses

%description -l uk.UTF-8
Цей пакет містить утиліти командного рядка для ALSA project:
- alsactl - утиліта для збереження/відновлення настанов звукової карти
- aplay/arecord - утиліта для запису/програвання файлів .wav, .voc,
  .au
- amixer - мікшер, який керується з командного рядка
- alsamixer - мікшер з інтерфейсом ncurses

%package init
Summary:	Init script for Advanced Linux Sound Architecture
Summary(pl.UTF-8):	Skrypt init dla Advanced Linux Sound Architecture
Group:		Applications/Sound
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description init
Init script for Advanced Linux Sound Architecture.

%description init -l pl.UTF-8
Skrypt init dla Advanced Linux Sound Architecture.

%prep
%setup -q

%build
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
CFLAGS="%{rpmcflags} -I/usr/include/ncurses"
CXXFLAGS="%{rpmcxxflags} -fno-rtti -fno-exceptions"
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/alsasound
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/alsa-oss-pcm

rm -f $RPM_BUILD_ROOT%{_mandir}/man1/arecord.1
echo ".so aplay.1" > $RPM_BUILD_ROOT%{_mandir}/man1/arecord.1

touch $RPM_BUILD_ROOT%{_sysconfdir}/asound.conf

%find_lang alsa-utils --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add alsasound
%service alsasound restart "ALSA %{version} services"

%preun init
if [ "$1" = "0" ]; then
	%service alsasound stop
	/sbin/chkconfig --del alsasound
fi

%files -f alsa-utils.lang
%defattr(644,root,root,755)
%doc README ChangeLog
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/asound.conf
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_datadir}/alsa/speaker-test
%{_datadir}/sounds/alsa
%{_mandir}/man1/aconnect.1*
%{_mandir}/man1/alsactl.1*
%{_mandir}/man1/alsamixer.1*
%{_mandir}/man1/amidi.1*
%{_mandir}/man1/amixer.1*
%{_mandir}/man1/aplay.1*
%{_mandir}/man1/aplaymidi.1*
%{_mandir}/man1/arecord.1*
%{_mandir}/man1/arecordmidi.1*
%{_mandir}/man1/aseqnet.1*
%{_mandir}/man1/aseqdump.1*
%{_mandir}/man1/iecset.1*
%{_mandir}/man1/speaker-test.1*
%{_mandir}/man8/alsaconf.8*
%lang(fr) %{_mandir}/fr/man8/alsaconf.8*

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
