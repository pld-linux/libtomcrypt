#
# Conditional build:
%bcond_without	ltm		# use LibTomMath for Math provider

Summary:	LibTomCrypt - fairly comprehensive, modular and portable cryptographic toolkit
Summary(pl.UTF-8):	LibTomCrypt - dość obszerna, modularna i przenośna biblioteka kryptograficzna
Name:		libtomcrypt
Version:	1.17
Release:	1.1
License:	Public Domain
Group:		Libraries
Source0:	http://libtom.org/files/crypt-%{version}.tar.bz2
# Source0-md5:	cea7e5347979909f458fe7ebb5a44f85
Patch0:		%{name}-link.patch
URL:		https://github.com/libtom/libtomcrypt
%{?with_ltm:BuildRequires:	libtommath-devel}
BuildRequires:	libtool >= 2:1.5
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

%description devel
Header files for LibTomCrypt library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki LibTomCrypt.

%package static
Summary:	Static LibTomCrypt library
Summary(pl.UTF-8):	Statyczna biblioteka LibTomCrypt
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static LibTomCrypt library.

%description static -l pl.UTF-8
Statyczna biblioteka LibTomCrypt.

%prep
%setup -q
%patch0 -p1

%build
CFLAGS="%{rpmcflags} %{?with_ltm:-DLTC_NO_ASM -DUSE_LTM -DLTM_DESC}" \
%{?with_ltm:EXTRALIBS=-ltommath} \
%{__make} -f makefile.shared \
	CC="libtool --mode=compile --tag=CC %{__cc}" \
	CCLD="libtool --mode=link --tag=CC %{__cc}" \
	LIBPATH=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -f makefile.shared install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBPATH=%{_libdir} \
	GROUP=$(id -ng) \
	USER=$(id -nu)

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE TODO changes
%attr(755,root,root) %{_libdir}/libtomcrypt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtomcrypt.so.0
%attr(755,root,root) %{_libdir}/libtomcrypt_prof.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtomcrypt_prof.so.0

%files devel
%defattr(644,root,root,755)
%doc doc/crypt.pdf notes/*.txt
%attr(755,root,root) %{_libdir}/libtomcrypt.so
%attr(755,root,root) %{_libdir}/libtomcrypt_prof.so
%{_libdir}/libtomcrypt.la
%{_libdir}/libtomcrypt_prof.la
%{_includedir}/tomcrypt*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libtomcrypt.a
%{_libdir}/libtomcrypt_prof.a
