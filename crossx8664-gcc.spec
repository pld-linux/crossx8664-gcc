#
# TODO:
#		- symlinks {lib64,ld-*}
#
Summary:	Cross AMD64 GNU binary utility development utilities - gcc
Summary(es):	Utilitarios para desarrollo de binarios de la GNU - AMD64 gcc
Summary(fr):	Utilitaires de d�veloppement binaire de GNU - AMD64 gcc
Summary(pl):	Skro�ne narz�dzia programistyczne GNU dla AMD64 - gcc
Summary(pt_BR):	Utilit�rios para desenvolvimento de bin�rios da GNU - AMD64 gcc
Summary(tr):	GNU geli�tirme ara�lar� - AMD64 gcc
Name:		crossamd64-gcc
%define		_snap	20040820
Version:	3.4.2
Release:	0.%{_snap}.1
Epoch:		1
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/snapshots/3.4-%{_snap}/gcc-3.4-%{_snap}.tar.bz2
# Source0-md5:	1ac3d6a9b67ee2e55a5448dc7a1996cc
BuildRequires:	crossamd64-binutils
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	autoconf
BuildRequires:	/bin/bash
Requires:	crossamd64-binutils
ExcludeArch:	amd64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		amd64-pld-linux
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_libdir}/gcc/%{target}
%define		gcclib		%{gccarch}/%{version}

%define		_noautostrip	.*%{gcclib}.*/libgcc\\.a

%description
This package contains a cross-gcc which allows the creation of
binaries to be run on AMD64 linux (architecture amd64-linux) on
other machines.

%description -l de
Dieses Paket enth�lt einen Cross-gcc, der es erlaubt, auf einem
anderem Rechner Code f�r amd64-Linux zu generieren.

%description -l pl
Ten pakiet zawiera skro�ny gcc pozwalaj�cy na robienie na innych
maszynach binari�w do uruchamiania na AMD64 (architektura
amd64-linux).

%prep
%setup -q -n gcc-3.4-%{_snap}

%build
rm -rf obj-%{target}
install -d obj-%{target}
cd obj-%{target}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false \
../configure \
	--prefix=%{_prefix} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--disable-shared \
	--disable-threads \
	--enable-languages="c" \
	--with-gnu-as \
	--with-gnu-ld \
	--with-system-zlib \
	--with-multilib \
	--with-newlib \
	--without-headers \
	--without-x \
	--target=%{target} \
	--host=%{_target_platform} \
	--build=%{_target_platform}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C obj-%{target} install \
	DESTDIR=$RPM_BUILD_ROOT

# don't want this here
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

%if 0%{!?debug:1}
%{target}-strip -g $RPM_BUILD_ROOT%{gcclib}/libgcc.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{target}-cpp
%attr(755,root,root) %{_bindir}/%{target}-gcc*
%attr(755,root,root) %{_bindir}/%{target}-gcov
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%{gcclib}/crt*.o
%{gcclib}/libgcc.a
%{gcclib}/specs*
%dir %{gcclib}/32
%{gcclib}/32/crt*.o
%{gcclib}/32/libgcc.a
%dir %{gcclib}/include
%{gcclib}/include/*.h
%{_mandir}/man1/%{target}-gcc.1*
