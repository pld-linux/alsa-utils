Summary:	Advanced Linux Sound Architecture (ALSA) - Utils
Summary(es):	Utilitarios para ALSA (Advanced Linux Sound Architecture)
Summary(pl):	Advanced Linux Sound Architecture (ALSA) - Narz�dzia
Summary(pt_BR):	Utilit�rios para o ALSA (Advanced Linux Sound Architecture)
Summary(ru):	������� ��������� ������ ��� ALSA project
Summary(uk):	���̦�� ���������� ����� ��� ALSA project
Name:		alsa-utils
Version:	1.0.8
Release:	1
License:	GPL
Group:		Applications/Sound
Source0:	ftp://ftp.alsa-project.org/pub/utils/%{name}-%{version}.tar.bz2
# Source0-md5:	c72d0efa9c88770a10733ec2abc1a872
Source1:	alsasound.init
Source2:	alsa-oss-pcm
Patch0:		%{name}-alsaconf.patch
URL:		http://www.alsa-project.org/
BuildRequires:	alsa-lib-devel >= 1.0.3
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	ncurses-devel
Requires:	awk
Requires:	dialog
Requires:	diffutils
Requires:	which
Obsoletes:	alsaconf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This packages contains command line utilities for the ALSA project:
- alsactl	- utility for store / restore of soundcard settings
- aplay/arecord	- utility for playback / record of .wav, .voc, .au files
- amixer	- a command line mixer
- alsamixer	- ncurses mixer

%description -l es
Utilitarios para el sistema ALSA, la arquitetura avanzada de sonido
para Linux.

%description -l pl
Pakiet zawiera nast�puj�ce, dzia�aj�ce z linii polece�, narz�dzia dla
projektu ALSA (Advanced Linux Sound Architecture):
- alsactl	- narz�dzie do zapami�tywania / przywracania ustawie�
		  karty d�wi�kowej
- aplay/arecord	- narz�dzia do odtwarzania / nagrywania plik�w .wav,
		  .voc, .au
- amixer	- mikser dzia�aj�cy z linii polece�
- alsamixer	- mikser z interfejsem opartym o ncurses

%description -l pt_BR
Utilit�rios para o ALSA, a arquitetura de som avan�ada para o Linux.

%description -l ru
���� ����� �������� ������� ��������� ������ ��� ALSA project:
- alsactl	- ������� ��� ����������/�������������� ��������
		  �������� �����
- aplay/arecord	- ������� ��� ������/������������ ������ .wav, .voc,
		  .au
- amixer	- ������, ����������� �� ��������� ������
- alsamixer	- ������ � ����������� ncurses

%description -l uk
��� ����� ͦ����� ���̦�� ���������� ����� ��� ALSA project:
- alsactl	- ���̦�� ��� ����������/צ��������� ��������
		  ������ϧ �����
- aplay/arecord	- ���̦�� ��� ������/����������� ���̦� .wav, .voc,
		  .au
- amixer	- ͦ����, ���� ���դ���� � ���������� �����
- alsamixer	- ͦ���� � ����������� ncurses

%package init
Summary:	Init script for Advanced Linux Sound Architecture
Summary(pl):	Skrypt init dla Advanced Linux Sound Architecture
Group:		Applications/Sound
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}

%description init
Init script for Advanced Linux Sound Architecture.

%description init -l pl
Skrypt init dla Advanced Linux Sound Architecture.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
CFLAGS="%{rpmcflags} -I/usr/include/ncurses"
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-exceptions"
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

%clean
rm -rf $RPM_BUILD_ROOT

%post init
/sbin/chkconfig --add alsasound
if [ -f /var/lock/subsys/alsasound ]; then
	/etc/rc.d/init.d/alsasound restart >&2
else
	echo "Run \"/etc/rc.d/init.d/alsasound start\" to start ALSA %{version} services."
fi

%preun init
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/alsasound ]; then
		/etc/rc.d/init.d/alsasound stop >&2
	fi
	/sbin/chkconfig --del alsasound
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/asound.conf
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*

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
%{_mandir}/man1/iecset.1*
%{_mandir}/man8/alsaconf.8*

%files init
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/*
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*
