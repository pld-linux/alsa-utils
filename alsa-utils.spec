Summary:	Advanced Linux Sound Architecture (ALSA) - Utils
Summary(es.UTF-8):	Utilitarios para ALSA (Advanced Linux Sound Architecture)
Summary(pl.UTF-8):	Advanced Linux Sound Architecture (ALSA) - Narzędzia
Summary(pt_BR.UTF-8):	Utilitários para o ALSA (Advanced Linux Sound Architecture)
Summary(ru.UTF-8):	Утилиты командной строки для ALSA project
Summary(uk.UTF-8):	Утиліти командного рядка для ALSA project
Name:		alsa-utils
Version:	1.0.27
Release:	2
# some apps GPL v2, some GPL v2+
License:	GPL v2
Group:		Applications/Sound
Source0:	ftp://ftp.alsa-project.org/pub/utils/%{name}-%{version}.tar.bz2
# Source0-md5:	cbfb21a24f63fb052b3392195639ce48
Source1:	alsasound.init
# does anything use this (probably outdated) file? not alsasound.init
Source2:	alsa-oss-pcm
Source3:	alsactl.conf
Patch0:		%{name}-fast_sampling.patch
Patch1:		%{name}-modprobe.patch
Patch2:		%{name}-build.patch
URL:		http://www.alsa-project.org/
BuildRequires:	alsa-lib-devel >= 1.0.26
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	gettext-devel >= 0.15
BuildRequires:	libsamplerate-devel >= 0.1.3
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	ncurses-ext-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	xmlto
Requires:	alsa-lib >= 1.0.26
Requires:	awk
Requires:	dialog
Requires:	diffutils
Requires:	systemd-units >= 0.38
Requires:	which
Suggests:	gpm
Obsoletes:	alsa-udev
Obsoletes:	alsaconf
Obsoletes:	udev-alsa
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
Requires:	systemd-units
Obsoletes:	alsa-udev

%description init
Init script for Advanced Linux Sound Architecture.

%description init -l pl.UTF-8
Skrypt init dla Advanced Linux Sound Architecture.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
CFLAGS="%{rpmcflags} -I/usr/include/ncurses"
CXXFLAGS="%{rpmcxxflags} -fno-rtti -fno-exceptions"
# we need alsactl for udev as early as possible
%configure \
	--sbindir=/sbin \
	--with-systemdsystemunitdir=%{systemdunitdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/alsasound
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/alsa-oss-pcm
install -D %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/alsa/alsactl.conf

install -d $RPM_BUILD_ROOT/lib/alsa
mv $RPM_BUILD_ROOT%{_datadir}/alsa/init $RPM_BUILD_ROOT/lib/alsa

ln -s /lib/alsa/init $RPM_BUILD_ROOT%{_datadir}/alsa/init
install -d $RPM_BUILD_ROOT%{_sbindir}
ln -s /sbin/alsactl $RPM_BUILD_ROOT%{_sbindir}/alsactl

%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/arecord.1
echo ".so aplay.1" > $RPM_BUILD_ROOT%{_mandir}/man1/arecord.1

%find_lang alsa-utils --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
# this needs to be a dir
if [ -d %{_datadir}/alsa/init -a ! -h %{_datadir}/alsa/init ]; then
	mv -b %{_datadir}/alsa/init{,.dir}
%banner -e %{name} <<EOF
Check %{_datadir}/alsa/init.dir for your own files and remove it when done.
EOF
fi

%post init
/sbin/chkconfig --add alsasound
%service alsasound restart "ALSA %{version} services"

%preun init
if [ "$1" = "0" ]; then
	%service alsasound stop
	/sbin/chkconfig --del alsasound
fi

%triggerpostun -- %{name} < 1.0.24.2-2
install -d /var/lib/alsa
if [ -f /etc/asound.state ]; then
	mv -f /etc/asound.state /var/lib/alsa/asound.state
fi

%files -f alsa-utils.lang
%defattr(644,root,root,755)
%doc ChangeLog README TODO
%attr(755,root,root) /sbin/alsaconf
%attr(755,root,root) /sbin/alsactl
%attr(755,root,root) %{_bindir}/aconnect
%attr(755,root,root) %{_bindir}/alsaloop
%attr(755,root,root) %{_bindir}/alsamixer
%attr(755,root,root) %{_bindir}/alsaucm
%attr(755,root,root) %{_bindir}/amidi
%attr(755,root,root) %{_bindir}/amixer
%attr(755,root,root) %{_bindir}/aplay
%attr(755,root,root) %{_bindir}/aplaymidi
%attr(755,root,root) %{_bindir}/arecord
%attr(755,root,root) %{_bindir}/arecordmidi
%attr(755,root,root) %{_bindir}/aseqdump
%attr(755,root,root) %{_bindir}/aseqnet
%attr(755,root,root) %{_bindir}/iecset
%attr(755,root,root) %{_bindir}/speaker-test
# symlink
%attr(755,root,root) %{_sbindir}/alsactl
%{_sysconfdir}/alsa/alsactl.conf
%{systemdunitdir}/alsa-restore.service
%{systemdunitdir}/alsa-store.service
%{systemdunitdir}/basic.target.wants/alsa-restore.service
%{systemdunitdir}/shutdown.target.wants/alsa-store.service
/lib/udev/rules.d/90-alsa-restore.rules
%dir /var/lib/alsa
%dir /lib/alsa
/lib/alsa/init
%{_datadir}/alsa/init
%{_datadir}/alsa/speaker-test
%{_datadir}/sounds/alsa
%{_mandir}/man1/aconnect.1*
%{_mandir}/man1/alsactl.1*
%{_mandir}/man1/alsaloop.1*
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
%{_mandir}/man7/alsactl_init.7*
%{_mandir}/man8/alsaconf.8*
%lang(fr) %{_mandir}/fr/man8/alsaconf.8*

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/alsasound
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/alsa-oss-pcm
%{systemdunitdir}/alsa-state.service
%{systemdunitdir}/basic.target.wants/alsa-state.service
