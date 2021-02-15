#
# Conditional build:
%bcond_without	tests		# build without tests
%bcond_without	unibilium

Summary:	Library for easy processing of keyboard entry from terminal-based programs
Name:		libtermkey
Version:	0.20
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://www.leonerd.org.uk/code/libtermkey/%{name}-%{version}.tar.gz
# Source0-md5:	710ee4e48d8550e65f3adf627aac8465
Patch0:		0001-build-take-into-account-CFLAGS-LDFLAGS-for-tests.patch
Patch1:		0002-include-stdlib.h-for-putenv.patch
URL:		http://www.leonerd.org.uk/code/libtermkey/
BuildRequires:	gcc
BuildRequires:	libtool
BuildRequires:	pkgconfig
%if %{with unibilium}
BuildRequires:	unibilium-devel >= 0.1.0
%else
BuildRequires:	pkgconfig(tinfo)
%endif
%if %{with tests}
BuildRequires:	/usr/bin/prove
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library allows easy processing of keyboard entry from
terminal-based programs. It handles all the necessary logic to
recognise special keys, UTF-8 combining, and so on, with a simple
interface.

%package devel
Summary:	Development files needed for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files needed for %{name}.

%prep
%setup -q

# No need for demos
%{__sed} -i -e '/^all:/s/$(DEMOS)//' Makefile

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	VERBOSE=1

%if %{with tests}
%{__make} test \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	VERBOSE=1
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

rm -vf $RPM_BUILD_ROOT%{_libdir}/*.{a,la}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE
%attr(755,root,root) %{_libdir}/libtermkey.so.*.*.*
%{_libdir}/libtermkey.so.1

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtermkey.so
%{_includedir}/termkey.h
%{_pkgconfigdir}/termkey.pc
%{_mandir}/man3/termkey_*.3*
%{_mandir}/man7/termkey.7*
