%define debug_package %{nil}
%define _enable_debug_packages %{nil}

%{?_compat_el5_build}

%{!?scl:%global scl autotools-latest}

%{?scl:%scl_package m4}

# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4590 for more details
%define release_prefix 8

Summary: The GNU macro processor
Name: autotools-latest-m4
Version: 1.4.18
Release: %{release_prefix}%{?dist}.cpanel
License: GPLv3+
Group: Applications/Text
Source0: http://ftp.gnu.org/gnu/m4/m4-%{version}.tar.gz
Source1: http://ftp.gnu.org/gnu/m4/m4-%{version}.tar.gz.sig
URL: http://www.gnu.org/software/m4/

%if 0%{?rhel} > 7
Patch0: 0001-Fix-file-io-libs-for-newer-gnulib.patch
%endif

%if 0%{?rhel} >= 9
Patch1: 0002-Remove-troublesome-code-for-Alma-9-and-above.patch
%endif

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
%ifarch ppc ppc64
BuildRequires: texinfo
%endif

# Gnulib bundled - the library has been granted an exception, see https://fedorahosted.org/fpc/ticket/174
# Gnulib is not versioned, see m4 ChangeLog for approximate date of Gnulib copy
Provides: bundled(gnulib)

%{?scl:
BuildRequires: scl-utils-build
Requires:%scl_runtime
}

# RHEL5 WA for not-defined buildroot
%if ! 0%{?buildroot:1}
BuildRoot: %{_tmppath}/%{name}-%{version}-root
%global buildroot %{_tmppath}/%{name}-%{version}-root
%endif

%description
A GNU implementation of the traditional UNIX macro processor.  M4 is
useful for writing text files which can be logically parsed, and is used
by many programs as part of their build process.  M4 has built-in
functions for including files, running shell commands, doing arithmetic,
etc.  The autoconf program needs m4 for generating configure scripts, but
not for running configure scripts.

Install m4 if you need a macro processor.

%prep
%setup -q -n m4-%{version}
chmod 644 COPYING

%if 0%{?rhel} > 7
%patch0 -p1
%endif

%if 0%{?rhel} >= 9
%patch1 -p1
%endif

%build
set -x

%configure

make %{?_smp_mflags}

%install
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%check
make %{?_smp_mflags} check

%files
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO
%{_bindir}/m4
%{_infodir}/*
%{_mandir}/man1/m4.1*

%post
if [ -f %{_infodir}/m4.info.gz ]; then # --excludedocs?
    /sbin/install-info %{_infodir}/m4.info.gz %{_infodir}/dir || :
fi

%preun
if [ "$1" = 0 ]; then
    if [ -f %{_infodir}/m4.info.gz ]; then # --excludedocs?
        /sbin/install-info --delete %{_infodir}/m4.info.gz %{_infodir}/dir || :
    fi
fi


%changelog
* Wed Aug 02 2023 Dan Muey <dan@cpanel.net> - 1.4.18-8
- ZC-11101: Fix unresolvable `Name` (by hard coding it)

* Wed May 17 2023 Julian Brown <julian.brown@cpanel.net> - 1.4.18-7
- ZC-10950: Fix build problems

* Tue May 09 2023 Brian Mendoza <brian.mendoza@cpanel.net> - 1.4.18-6
- ZC-10936: Clean up Makefile and remove debug-package-nil

* Thu Sep 29 2022 Julian Brown <julian.brown@cpanel.net> - 1.4.17-5
- ZC-10336: Add changes so that it builds on AlmaLinux 9

* Thu May 21 2020 Julian Brown <julian.brown@cpanel.net> - 1.4.17-4
- ZC-6855: Fix build issues for C8

* Wed Aug 12 2015 Pavel Raiskup <praiskup@redhat.com> - 1.4.17-3
- use _compat_el5_build only if defined (rhbz#1252751)

* Thu May 29 2014 Pavel Raiskup <praiskup@redhat.com> - 1.4.17-2
- release bump for %%_compat_el5_build

* Tue Mar 25 2014 Pavel Raiskup <praiskup@redhat.com> - 1.4.17-1
- SCLized spec file from rawhide
