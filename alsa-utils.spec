Summary:	Advanced Linux Sound Architecture (ALSA) - Utils
Summary(pl):	Advanced Linux Sound Architecture (ALSA) - Narzêdzia
Name:		alsa-utils
Version:	0.3.0-pre3
Release:	1d
Copyright:	GPL
Group:		Applications/Sound
Group(pl):	Aplikacje/D¼wiêk
Vendor:		Jaroslav Kysela <perex@jcu.cz>
Source:		ftp://alsa.jcu.cz/pub/utils/%{name}-%{version}.tar.gz 
BuildRoot:	/tmp/buildroot-%{name}-%{version}
URL:		http://alsa.jcu.cz
Requires:	alsa-driver
Requires:	alsa-lib
Patch0:		%{name}-noroot.patch
Patch1:		%{name}-opt.patch

%description
Advanced Linux Sound Architecture (ALSA) - Utils
alsamixer, amixer, aplay, arecord

%description -l pl
Advanced Linux Sound Architecture (ALSA) - Narzêdzia
alsamixer, amixer, aplay, arecord

%prep
%setup -q 
%patch0 -p1
%patch1 -p1

%build
./configure --prefix=/usr
OPT="$RPM_OPT_FLAGS" make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/usr/{bin,man/man1}
make prefix=$RPM_BUILD_ROOT/usr install

rm -f $RPM_BUILD_ROOT/usr/man/man1/aplay.1

echo ".so arecord.1" > $RPM_BUILD_ROOT/usr/man/man1/aplay.1

strip $RPM_BUILD_ROOT/usr/{s,}bin/*

bzip2 -9  README ChangeLog amixer/README.first 
gzip -9fn $RPM_BUILD_ROOT/usr/man/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,ChangeLog}.bz2 amixer/README.first.bz2

%attr(755,root,root) /usr/bin/*
%attr(755,root,root) /usr/sbin/*
%attr(644,root, man) /usr/man/man1/*

%changelog
* Wed Jan 27 1999 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [0.3.0-pre3-1d]
- new upstream release

* Tue Jan 05 1999 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
- alsactl was missing !
- added optimalization

* Mon Sep 28 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
- changed "-" to "_" (rpm doesn't like "-" in Name: or Version:)

* Sun Sep 27 1998 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
- rewrited spec file

* Mon May 28 1998 Helge Jensen <slog@slog.dk>
- Made SPEC file
