%define _prefix /usr

%define debug 0
%define final 0

%define alsa 1
%define qt_version 3.3.5

%define make_cvs 1
%define disable_gcc_check_and_hidden_visibility 1

Version: 1.5.2
Release: 1
Summary: aRts (analog realtime synthesizer) - the KDE sound system
Name: arts
Group: System Environment/Daemons
License: LGPL
Epoch: 8
Url: http://www.kde.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/%{name}-%{version}.tar.bz2

Patch0: kde-libtool.patch
Patch1: arts-1.1.4-debug.patch
Patch2: arts-1.3.92-glib2.patch
Patch5: arts-1.3.1-alsa.patch
Patch6: arts-1.4.0-glibc.patch
Patch7: arts-1.5.0-check_tmp_dir.patch

Prereq: /sbin/ldconfig
Requires: audiofile
Obsoletes: kdelibs-sound
Provides: kdelibs-sound

%if %{alsa}
BuildRequires: alsa-lib-devel >= 1.0.2
%endif
BuildRequires: autoconf >= 2.53
BuildRequires: automake
BuildRequires: qt-devel >= 1:%{qt_version}
BuildRequires: perl
BuildRequires: glib2-devel
BuildRequires: libvorbis-devel
BuildRequires: audiofile-devel
BuildRequires: esound-devel

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
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: esound-devel
Requires: glib2-devel
Requires: libvorbis-devel
Requires: audiofile-devel
%if %{alsa}
Requires: alsa-lib-devel
%endif
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
%patch0 -p1 -b .libtool
%patch1 -p1 -b .debug
%patch2 -p1 -b .glib
%patch5 -p1 -b .alsa
%patch6 -p1 -b .glibc
%patch7 -p1 -b .check_tmp_dir

%build
unset QTDIR && . /etc/profile.d/qt.sh
FLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$FLAGS"
export CFLAGS="$FLAGS"
export PATH=`pwd`:$PATH

%if %{make_cvs}
  make -f admin/Makefile.common cvs
%endif

%configure \
   --enable-new-ldflags \
   --disable-dependency-tracking \
%if %{disable_gcc_check_and_hidden_visibility}
   --disable-gcc-hidden-visibility \
%endif
%if %{alsa}
   --with-alsa \
%endif
%if %{final}
   --enable-final \
%endif
   --includedir=%{_includedir}/kde \
   --with-qt-libraries=$QTDIR/lib \
   --disable-debug \
   --disable-warnings \
   --disable-rpath

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

export PATH=`pwd`:$PATH
export DESTDIR=$RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
chmod a+x $RPM_BUILD_ROOT%{_libdir}/*

# work around for rpm bug on s390x
%ifarch s390x
strip $RPM_BUILD_ROOT%{_bindir}/mcopidl
%endif

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
%{_libdir}/lib*.so.*
%{_bindir}/artscat
%{_bindir}/artsd
%{_bindir}/artsdsp
%{_bindir}/artsplay
%{_bindir}/artsrec
%{_bindir}/artsshell
%{_bindir}/artswrapper

%files devel
%defattr(-,root,root)
%{_bindir}/mcopidl
%{_libdir}/lib*.so
%{_includedir}/kde/arts
%{_includedir}/kde/artsc
%{_bindir}/artsc-config

%changelog
* Tue Mar 21 2006 Than Ngo <than@redhat.com> 8:1.5.2-1
- update to 1.5.2

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 8:1.5.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 8:1.5.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Feb 01 2006 Than Ngo <than@redhat.com> 8:1.5.1-1
- 1.5.1

* Wed Jan 18 2006 Than Ngo <than@redhat.com> 8:1.5.0-2
- rebuilt with --enable-new-ldflags

* Mon Dec 19 2005 Than Ngo <than@redhat.com> 8:1.5.0-1
- apply patch to fix #169631 

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 24 2005 Than Ngo <than@redhat.com> 8:1.5.0-0.1.rc2
- update to 3.5.0 rc2

* Mon Nov 14 2005 Than Ngo <than@redhat.com> 8:1.5.0-0.1.rc1
- update to 3.5.0 rc1
- another patch to fix lnusertemp problem

* Fri Nov 04 2005 Than Ngo <than@redhat.com> 8:1.4.92-2
- fix lnusertemp problem #169631

* Mon Oct 24 2005 Than Ngo <than@redhat.com> 8:1.4.92-1
- update to KDE 3.5 beta2

* Tue Sep 27 2005 Than Ngo <than@redhat.com> 8:1.4.91-1
- update to KDE 3.5 beta1
- drop multilib and pie patches which are included in new upstream

* Mon Aug 01 2005 Than Ngo <than@redhat.com> 8:1.4.2-1
- update to 1.4.2

* Tue Jun 21 2005 Than Ngo <than@redhat.com> 8:1.4.1-2 
- rebuilt

* Mon Jun 06 2005 Than Ngo <than@redhat.com> 8:1.4.1-1
- 1.4.1

* Thu Mar 17 2005 Than Ngo <than@redhat.com> 8:1.4.0-1
- KDE 3.4.0 release

* Mon Mar 14 2005 Than Ngo <than@redhat.com> 8:1.4.0-0.rc1.5
- fix build problem

* Fri Mar 04 2005 Than Ngo <than@redhat.com> 8:1.4.0-0.rc1.4
- rebuilt against gcc-4.0.0-0.31

* Tue Mar 01 2005 Than Ngo <than@redhat.com> 8:1.4.0-0.rc1.3
- rebuilt against gcc 4

* Fri Feb 25 2005 Than Ngo <than@redhat.com> 8:1.4.0-0.rc1.2
- KDE 3.4.0 rc1

* Mon Feb 14 2005 Than Ngo <than@redhat.com> 8:1.3.92-0.1
- 3.4beta2

* Fri Dec 03 2004 Than Ngo <than@redhat.com> 8:1.3.2-0.1
- update to KDE 3.3.2

* Fri Nov 19 2004 Than Ngo <than@redhat.com> 8:1.3.1-4
- alsa as default

* Fri Oct 29 2004 Than Ngo <than@redhat.com> 8:1.3.1-3
- rebuilt in fc4 tree

* Sat Oct 16 2004 Than Ngo <than@redhat.com> 8:1.3.1-2
- rebuilt for rhel

* Wed Oct 06 2004 Than Ngo <than@redhat.com> 1.3.1-1
- update to KDE 3.3.1

* Wed Sep 15 2004 Than Ngo <than@redhat.com> 1.3.0-4 
- fix multilib problem #132576

* Fri Sep 03 2004 Colin Walters <walters@redhat.com> 1.3.0-3
- Fix trivial conflict in glib patch and reapply; this
  removes dependency on glib2.0 and therefore prevents
  symbol clashes with applications loading arts still
  using glib 1.2, like XMMS.

* Mon Aug 23 2004 Than Ngo <than@redhat.com> 1.3.0-2
- add missing epoch tag

* Thu Aug 19 2004 Than Ngo <than@redhat.com> 1.3.0-1
- update to 1.3.0 release

* Tue Aug 10 2004 Than Ngo <than@redhat.com> 1.3.0-0.1.rc2
- update 3.3 rc2

* Sun Aug 08 2004 Than Ngo <than@redhat.com> 1.3.0-0.1.rc1
- update to 3.3 rc1 

* Tue Aug 03 2004 Than Ngo <than@redhat.com> 1.2.92-1.1
- update to 3.3 beta2

* Wed Jun 30 2004 Than Ngo <than@redhat.com> 1.2.91-1
- update to 3.3 beta1

* Mon Jun 28 2004 Than Ngo <than@redhat.com> 1.2.3-3
- add buildrequires on esound-devel (bug #125293)

* Thu Jun 17 2004 Than Ngo <than@redhat.com> 1.2.3-2
- rebuild

* Mon May 31 2004 Than Ngo <than@redhat.com> 1.2.3-1
- update to 1.2.3

* Thu May 13 2004 Than Ngo <than@redhat.com> 1.2.2-3
- add patch to enable PIE build of artsd

* Mon Apr 19 2004 Than Ngo <than@redhat.com> 1.2.2-2
- #120265 #119642 -devel req alsa-lib-devel esound-devel glib2-devel

* Mon Apr 12 2004 Than Ngo <than@redhat.com> 1.2.2-1
- 1.2.2 release

* Fri Apr 02 2004 Than Ngo <than@redhat.com> 1.2.1-2
- add several fixes from stable branch

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Than Ngo <than@redhat.com> 1.2.1-1
- update to 1.2.1

* Mon Feb 23 2004 Than Ngo <than@redhat.com> 8:1.2.0-1.5
- add patch file from CVS, fix mcop warning
- fix glib2 issue

* Tue Feb 17 2004 Than Ngo <than@redhat.com> 1.2.0-1.4 
- add missing build requirements
- add patch file from Bero #115507

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 05 2004 Than Ngo <than@redhat.com> 1.2.0-0.3 
- rebuilt against qt 3.3.0

* Tue Feb 03 2004 Than Ngo <than@redhat.com> 8:1.2.0-0.1
- 3.2.0 release

* Mon Jan 19 2004 Than Ngo <than@redhat.com> 8:1.1.95-0.1
- KDE 3.2RC1

* Fri Dec 12 2003 Than Ngo <than@redhat.com> 8:1.1.94-0.2
- rebuild against alsa-lib 1.0.0

* Mon Dec 01 2003 Than Ngo <than@redhat.com> 8:1.1.94-0.1
- KDE 3.2 beta2

* Wed Nov 26 2003 Than Ngo <than@redhat.com> 8:1.1.93-0.4
- disable rpath

* Wed Nov 26 2003 Than Ngo <than@redhat.com> 8:1.1.93-0.3
- rebuild to fix dependant libraries check on x86_64

* Tue Nov 25 2003 Than Ngo <than@redhat.com> 8:1.1.93-0.2
- enable support alsa

* Fri Oct 31 2003 Than Ngo <than@redhat.com> 8:1.1.93-0.1
- KDE 3.2 beta1
- remove some unneeded patch, which are now in new upstream

* Tue Oct 14 2003 Than Ngo <than@redhat.com> 8:1.2-0.14_10_2003.1
- arts-1.2-14_10_2003

* Fri Oct 10 2003 Than Ngo <than@redhat.com> 8:1.1.4-2.1
- rebuilt against qt 3.2.1

* Mon Sep 29 2003 Than Ngo <than@redhat.com> 8:1.1.4-2
- arts_debug issue (bug #104278)

* Mon Sep 29 2003 Than Ngo <than@redhat.com> 8:1.1.4-1
- 3.1.4

* Thu Aug 28 2003 Than Ngo <than@redhat.com> 8:1.1.3-3
- rebuild

* Thu Jul 31 2003 Than Ngo <than@redhat.com> 8:1.1.3-2
- add workaround for gcc bug on ia64

* Tue Jul 29 2003 Than Ngo <than@redhat.com> 8:1.1.3-1
- add Prereq: /sbin/ldconfig

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
