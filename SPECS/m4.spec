%{?_compat_el5_build}

%{!?scl:%global scl autotools-latest}

%{?scl:%scl_package m4}

# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4590 for more details
%define release_prefix 3

Summary: The GNU macro processor
Name: %{scl_prefix}m4
Version: 1.4.17
Release: %{release_prefix}%{?dist}.cpanel
License: GPLv3+
Group: Applications/Text
Source0: http://ftp.gnu.org/gnu/m4/m4-%{version}.tar.gz
Source1: http://ftp.gnu.org/gnu/m4/m4-%{version}.tar.gz.sig
URL: http://www.gnu.org/software/m4/
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

%build
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
* Wed Aug 12 2015 Pavel Raiskup <praiskup@redhat.com> - 1.4.17-3
- use _compat_el5_build only if defined (rhbz#1252751)

* Thu May 29 2014 Pavel Raiskup <praiskup@redhat.com> - 1.4.17-2
- release bump for %%_compat_el5_build

* Tue Mar 25 2014 Pavel Raiskup <praiskup@redhat.com> - 1.4.17-1
- SCLized spec file from rawhide
