%define debug 0

%define qt_version 3.1.2

%define libtool 0

Version: 1.1.3
Release: 0.9x.1
Summary: aRts (analog realtime synthesizer) - the KDE sound system
Name: arts
Group: System Environment/Daemons
License: LGPL
Epoch: 8
Url: http://www.kde.org
BuildRoot: %{_tmppath}/%{name}-buildroot

Source: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2
Patch: arts-1.1.0-vacopy.patch
Patch1: arts-1.1-gcc3.patch
Patch2: kde-libtool.patch

Requires: audiofile

Obsoletes: kdelibs-sound

Provides: kdelibs-sound

BuildRequires: autoconf >= 2.53
BuildRequires: automake
BuildRequires: qt-devel >= %{qt_version}
BuildRequires: perl

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
requires: %{name} = %{epoch}:%{version}-%{release}
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
%setup -q
%patch -p1 -b .x86_64
%patch1 -p1 -b .gcc3
%patch2 -p1 -b .libtool

%build
unset QTDIR && . /etc/profile.d/qt.sh
FLAGS="$RPM_OPT_FLAGS -fno-exceptions -D_GNU_SOURCE"
export CXXFLAGS="$FLAGS -fno-use-cxa-atexit"
export CFLAGS="$FLAGS"
export PATH=`pwd`:$PATH

%configure \
   --includedir=%{_includedir}/kde \
   --with-qt-libraries=$QTDIR/lib \
   --disable-debug \
   --enable-final

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

export PATH=`pwd`:$PATH
export DESTDIR=$RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
chmod a+x $RPM_BUILD_ROOT%{_libdir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir %{_libdir}/mcop
%dir %{_libdir}/mcop/Arts
%{_libdir}/mcop/Arts/*
%{_libdir}/mcop/*.mcopclass
%{_libdir}/mcop/*.mcoptype
%{_libdir}/*.la
%{_bindir}/artscat
%{_bindir}/artsd*
%{_bindir}/artsp*
%{_bindir}/artss*
%{_bindir}/artsw*
%{_bindir}/artsr*
%{_bindir}/testdhandle
%{_libdir}/lib*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/mcopidl
%{_libdir}/lib*.so
%{_includedir}/kde/arts
%{_includedir}/kde/artsc
%{_bindir}/artsc-config

%changelog
* Wed Jul 16 2003 Than Ngo <than@redhat.com> 8:1.1.3-0.9x.1
- 3.1.3

* Wed Apr  2 2003 Than Ngo <than@redhat.com> 1.1.1-0.9x.1
- 3.1.1 for RHL 9

* Wed Mar  5 2003 Than Ngo <than@redhat.com> 1.1-8
- move la files in arts package (bug #83607)
- add better patch to get rid of gcc path from la file

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- debuginfo rebuild

* Thu Feb 20 2003 Than Ngo <than@redhat.com> 1.1-6
- rebuid against gcc 3.2.2 to fix dependency in la file

* Thu Feb 13 2003 Thomas Woerner <twoerner@redhat.com> 1.1-5
- fixed artsbuilder crash (#82750)

* Wed Jan 29 2003 Than Ngo <than@redhat.com> 1.1-4
- 3.1 release

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Than Ngo <than@redhat.com> 1.1-3
- update to rc7
- change version, increase Epoch

* Tue Dec  3 2002 Than Ngo <than@redhat.com> 1.1.0-2
- use %%configure

* Fri Nov 22 2002 Than Ngo <than@redhat.com> 1.1.0-1
- update to 1.1.0

* Sat Nov  9 2002 Than Ngo <than@redhat.com> 1.0.5-1
- update 1.0.5

* Fri Nov  8 2002 Than Ngo <than@redhat.com> 1.0.4-2.1
- fix build problem on x86_64

* Fri Nov  8 2002 Than Ngo <than@redhat.com> 1.0.4-2
- fix build problem

* Mon Oct 14 2002 Than Ngo <than@redhat.com> 1.0.4-1
- 1.0.4
- cleanup specfile

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
