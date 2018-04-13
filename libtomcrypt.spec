#
# Conditional build:
%bcond_without	ltm		# use LibTomMath for Math provider

Summary:	LibTomCrypt - fairly comprehensive, modular and portable cryptographic toolkit
Summary(pl.UTF-8):	LibTomCrypt - dość obszerna, modularna i przenośna biblioteka kryptograficzna
Name:		libtomcrypt
Version:	1.18.1
Release:	1
License:	Public Domain or WTFPL v2
Group:		Libraries
#Source0Download: https://github.com/libtom/libtomcrypt/releases
Source0:	https://github.com/libtom/libtomcrypt/releases/download/v%{version}/crypt-%{version}.tar.xz
# Source0-md5:	81dcf5cda845ebce5d42446615deb563
Patch0:		%{name}-pc.patch
URL:		http://www.libtom.net/LibTomCrypt/
%{?with_ltm:BuildRequires:	libtommath-devel >= 1.0.1}
BuildRequires:	libtool >= 2:1.5
%{?with_ltm:BuildRequires:	pkgconfig}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibTomCrypt is a fairly comprehensive, modular and portable
cryptographic toolkit that provides developers with a vast array of
well known published block ciphers, one-way hash functions, chaining
modes, pseudo-random number generators, public key cryptography and a
plethora of other routines.

%description -l pl.UTF-8
LibTomCrypt to dość obszerna, modularna i przenośna biblioteka
kryptograficzna, zapewniająca programistom szeroki zbiór dobrze
znanych szyfrów blokowych, jednokierunkowych funkcji haszujących,
trybów łańcuchowych, generatorów liczb pseudolosowych, kryptografii
klucza publicznego oraz wiele innych procedur.

%package devel
Summary:	Header files for LibTomCrypt library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki LibTomCrypt
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_ltm:Requires:	libtommath-devel}

%description devel
Header files for LibTomCrypt library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LibTomCrypt.

%package static
Summary:	Static LibTomCrypt library
Summary(pl.UTF-8):	Statyczna biblioteka LibTomCrypt
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
%{?with_ltm:Requires:	libtommath-static}

%description static
Static LibTomCrypt library.

%description static -l pl.UTF-8
Statyczna biblioteka LibTomCrypt.

%prep
%setup -q
%patch0 -p1

%build
# IGNORE_SPEED avoids overriding rpmcflags
CFLAGS="%{rpmcflags} %{?with_ltm:-DUSE_LTM -DLTM_DESC}" \
%{__make} -f makefile.shared \
	CC="%{__cc}" \
	IGNORE_SPEED=1 \
	LIBPATH=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -f makefile.shared install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	LIBPATH=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md changes
%attr(755,root,root) %{_libdir}/libtomcrypt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtomcrypt.so.1

%files devel
%defattr(644,root,root,755)
%doc doc/crypt.pdf notes/*.txt
%attr(755,root,root) %{_libdir}/libtomcrypt.so
%{_libdir}/libtomcrypt.la
%{_includedir}/tomcrypt*.h
%{_pkgconfigdir}/libtomcrypt.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libtomcrypt.a
