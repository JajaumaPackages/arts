%define is_release 1
%define beta %{nil}
%define rel 1
%define debug 0
%define DATE 20020807
Version: 1.0.3
%define ver %{version}%{beta}
Summary: aRts (analog realtime synthesizer) - the KDE sound system
#%if %{is_release}
#Source: ftp://ftp.kde.org/pub/kde/stable/%{version}/distribution/tar/generic/source/%{name}-%{ver}.tar.bz2
#%else
Source: cvs://cvs.kde.org/%{name}-%{DATE}.tar.bz2
#%endif
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
BuildRequires: autoconf >= 2.53 automake15 qt-devel >= 3.0.3-10

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

#%if %{is_release}
#%setup -q -n %{name}-%{ver}
#%else
%setup -q -n %{name}
#%endif

# Workaround for legacy auto* tools
[ -x /usr/bin/aclocal-1.5 ] && ln -s /usr/bin/aclocal-1.5 aclocal
[ -x /usr/bin/automake-1.5 ] && ln -s /usr/bin/automake-1.5 automake
export PATH=`pwd`:$PATH
# End workaround

make -f Makefile.cvs || :

%build
export PATH=`pwd`:$PATH
export FLAGS="$RPM_OPT_FLAGS -fno-rtti -fno-exceptions -fno-check-new -D_GNU_SOURCE"
unset QTDIR || : ; . /etc/profile.d/qt.sh

CXXFLAGS="$FLAGS" CFLAGS="$FLAGS" ./configure \
	--prefix=%{_prefix} \
	--disable-debug \
	--enable-final \
	--includedir=%{_includedir}/kde

make %{?_smp_mflags}

%install
export PATH=`pwd`:$PATH
export DESTDIR=$RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
chmod a+x $RPM_BUILD_ROOT%{_libdir}/*

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
%{_bindir}/artsc-config

%changelog
* Mon Aug 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.3-1
- 1.0.3

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Wed Aug  7 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.2-4
- Update to current KDE_3_0_BRANCH, should be pretty much the same
  as 1.0.3

* Mon Jul 22 2002 Tim Powers <timp@redhat.com> 1.0.2-3
- rebuild using gcc-3.2-0.1

* Mon Jul 22 2002 Than Ngo <than@redhat.com> 1.0.2-2
- Added some major bugfixes from 1.0.3

* Tue Jul  2 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.2-1
- 1.0.2

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 06 2002 Than Ngo <than@redhat.com> 1.0.1-5
- rebuild

* Wed May 29 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.1-4
- Source qt.sh

* Tue May 28 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.1-3
- Increase release number by 2 to work around build system breakage

* Fri May  9 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.1-1
- 1.0.1

* Wed May  7 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.0.0-6
- Update to current KDE_3_0_BRANCH

* Thu May 02 2002 Than Ngo <than@redhat.com> 1.0.0-5
- rebuild in against gcc-3.1-0.26/qt-3.0.3-12

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
