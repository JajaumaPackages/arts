%define is_release 1
%define beta %{nil}
%define rel 4
%define debug 0
%define DATE 20020326
Version: 1.0.0
%define ver %{version}%{beta}
Summary: aRts (analog realtime synthesizer) - the KDE sound system
%if %{is_release}
Source: ftp://ftp.kde.org/pub/kde/stable/%{version}/distribution/tar/generic/source/%{name}-%{ver}.tar.bz2
%else
Source: cvs://cvs.kde.org/%{name}-%{DATE}.tar.bz2
%endif
Name: arts
Epoch: 7
%if %{is_release}
%if "%{beta}" != ""
Release: 0.%{beta}.%{rel}
%else
Release: %{rel}
%endif
%else
Release: 0.cvs%{DATE}.%{rel}
%endif
Group: System Environment/Daemons
License: LGPL
BuildRoot: %{_tmppath}/%{name}-buildroot
Requires: audiofile
Obsoletes: kdelibs-sound
Provides: kdelibs-sound
BuildRequires: autoconf253 automake15 qt-devel >= 3.0.3-10
Source900: gccver.c
Provides: libartscbackend.so.0 libartsflow_idl.so.1 libartsflow.so.1 libartswavplayobject.so.0 libgmcop.so.1 libkmedia2_idl.so.1 libkmedia2.so.1 libmcop_mt.so.1 libmcop.so.1 libqtmcop.so.1 libsoundserver_idl.so.1 libx11globalcomm.so.1

%description
arts (analog real-time synthesizer) is the sound system of KDE 3.

The principle of arts is to create/process sound using small modules which do
certain tasks. These may be create a waveform (oscillators), play samples,
filter data, add signals, perform effects like delay/flanger/chorus, or
output the data to the soundcard.

By connecting all those small modules together, you can perform complex
tasks like simulating a mixer, generating an instrument or things like
playing a wave file with some effects.


%package devel
Group: Development/Libraries
Summary: Development files for the aRts sound server
Obsoletes: kdelibs-sound-devel
Provides: kdelibs-sound-devel

%description devel
arts (analog real-time synthesizer) is the sound system of KDE 3.

The principle of arts is to create/process sound using small modules which do
certain tasks. These may be create a waveform (oscillators), play samples,
filter data, add signals, perform effects like delay/flanger/chorus, or
output the data to the soundcard.

By connecting all those small modules together, you can perform complex
tasks like simulating a mixer, generating an instrument or things like
playing a wave file with some effects.

Install arts-devel if you intend to write applications using arts (such as
KDE applications using sound).

%prep
rm -rf $RPM_BUILD_ROOT

%if %{is_release}
%setup -q -n %{name}-%{ver}
%else
%setup -q -n %{name}
%endif

# Workaround for legacy auto* tools
[ -x /usr/bin/autoconf-2.5? ] && ln -s /usr/bin/autoconf-2.5? autoconf
[ -x /usr/bin/autoheader-2.5? ] && ln -s /usr/bin/autoheader-2.5? autoheader
[ -x /usr/bin/aclocal-1.5 ] && ln -s /usr/bin/aclocal-1.5 aclocal
[ -x /usr/bin/automake-1.5 ] && ln -s /usr/bin/automake-1.5 automake
export PATH=`pwd`:$PATH
# End workaround

make -f Makefile.cvs || :

%build
export PATH=`pwd`:$PATH
export FLAGS="$RPM_OPT_FLAGS -fno-rtti -fno-exceptions -fno-check-new -D_GNU_SOURCE"

CXXFLAGS="$FLAGS" CFLAGS="$FLAGS" ./configure \
	--prefix=%{_prefix} \
	--disable-debug \
	--enable-final \
	--includedir=%{_includedir}/kde

gcc -o gccver %{SOURCE900}
if [ "0`./gccver`" -lt 3001 ]; then
	find . -name Makefile |xargs perl -pi -e "s,^CXXLD\s*=.*,\$& -release gcc`./gccver -v`,g"
fi

make %{?_smp_mflags}

%install
export PATH=`pwd`:$PATH
export DESTDIR=$RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

export FLAGS="$RPM_OPT_FLAGS -fno-rtti -fno-exceptions -fno-check-new"
CXXFLAGS="$FLAGS" CFLAGS="$FLAGS" ./configure \
	--prefix=%{_prefix} \
	--enable-static \
	--disable-debug \
	--disable-shared \
	--enable-final

cd artsc
make clean
make
install -m 644 .libs/libartsc.a $RPM_BUILD_ROOT%{_libdir}
cd ..

chmod a+x $RPM_BUILD_ROOT%{_libdir}/*


# Set symlinks for files we renamed because of compiler ABI issues
if [ "0`./gccver`" -lt 3001 ]; then
        REL="gcc`./gccver -v`"
	solink() {
		sover=$1
		somajor=`echo $sover |sed -e "s,\..*,,"`
		shift
		for i in $@; do
			if [ -e $RPM_BUILD_ROOT/%{_libdir}/lib${i}-${REL}.so ]; then
				ln -s lib${i}-${REL}.so $RPM_BUILD_ROOT/%{_libdir}/lib${i}.so.${sover}
				ln -s lib${i}-${REL}.so $RPM_BUILD_ROOT/%{_libdir}/lib${i}.so.${somajor}
			elif [ -e $RPM_BUILD_ROOT%{_libdir}/lib${i}-${REL}.so.? ]; then
				ln -s `basename $RPM_BUILD_ROOT%{_libdir}/lib${i}-${REL}.so.?` $RPM_BUILD_ROOT/%{_libdir}/lib${i}.so.${sover}
				ln -s `basename $RPM_BUILD_ROOT%{_libdir}/lib${i}-${REL}.so.?` $RPM_BUILD_ROOT/%{_libdir}/lib${i}.so.${somajor}
			fi
		done
	}
	solink 0.0.0 artscbackend artswavplayobject
	solink 1.0.0 artsflow artsflow_idl gmcop kmedia2_idl kmedia2 mcop mcop_mt qtmcop soundserver_idl x11globalcomm
fi

%clean
# rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir %{_libdir}/mcop
%dir %{_libdir}/mcop/Arts
%{_libdir}/mcop/Arts/*
%{_libdir}/mcop/*.mcopclass
%{_libdir}/mcop/*.mcoptype
%{_bindir}/artscat
%{_bindir}/artsd*
%{_bindir}/artsp*
%{_bindir}/artss*
%{_bindir}/artsw*
%{_bindir}/artsr*
%{_libdir}/libartsc*.??*
%{_libdir}/libartsdsp*.*
%{_libdir}/libartsflow*.*
%{_libdir}/libartswav*.*
%{_libdir}/lib*mcop*.*
%{_libdir}/libx11globalcomm*.*
%{_libdir}/libsound*
%{_libdir}/libkmedia*

%files devel
%defattr(-,root,root)
%{_bindir}/mcopidl
%{_includedir}/kde/arts
%{_includedir}/kde/artsc
%{_libdir}/libartsc.a
%{_bindir}/artsc-config

%changelog
* Wed Apr 17 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.0-4
- Fix dangling symlink

* Mon Apr 15 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.0-3
- Change sonames to something indicating the compiler version if a compiler
  < gcc 3.1 is used
- Add compat symlinks for binary compatibility with other distributions

* Mon Apr  8 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.0-2
- Rebuild to get alpha binaries

* Wed Mar 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.0-1
- 1.0.0 final

* Tue Mar 19 2002 Bernhard Rosenkraenzer <bero@redhat.com> 0.9.9-0.cvs20020319.1
- aRts no longer uses the KDE version number; adapt spec file

* Wed Mar 13 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.cvs20020313.1
- Build with autoconf 2.53, automake 1.5

* Thu Feb 14 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.0.0-0.cvs20020114.1
- initial package
