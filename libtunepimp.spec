Summary:	The MusicBrainz tagging library
Summary(pl):	Biblioteka znakowania MusicBrainz
Name:		libtunepimp
Version:	0.4.0
Release:	1
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.musicbrainz.org/pub/musicbrainz/%{name}-%{version}.tar.gz
# Source0-md5:	c11c3082ee72896949cb4fdb7acbbf63
Patch0:		%{name}-readline.patch
Patch1:		%{name}-gcc4.patch
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	flac-devel
BuildRequires:	libid3tag-devel >= 0.15.0b
BuildRequires:	libmad-devel
BuildRequires:	libmusicbrainz-devel >= 2.1.0
BuildRequires:	libstdc++-devel >= 2:1.4d
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	readline-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The MusicBrainz tagging library.

%description -l pl
Biblioteka znakowania MusicBrainz.

%package devel
Summary:	Header files for libtunepimp library
Summary(pl):	Pliki nag³ówkowe biblioteki libtunepimp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libid3tag-devel
Requires:	libmad-devel
Requires:	libmusicbrainz-devel >= 2.1.0
Requires:	libstdc++-devel >= 2:1.4d
Requires:	libvorbis-devel

%description devel
Header files for libtunepimp library.

%description devel -l pl
Pliki nag³ówkowe biblioteki libtunepimp.

%package static
Summary:	Static libtunepimp library
Summary(pl):	Statyczna biblioteka libtunepimp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libtunepimp library.

%description static -l pl
Statyczna biblioteka libtunepimp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# not installed, but used by installed headers
install lib/threads/posix/mutex.h \
	lib/{analyzer,filecache,filelookup,lookup,plugins,readmeta,submit,write}.h \
	include/tunepimp/metadata.h \
	$RPM_BUILD_ROOT%{_includedir}/tunepimp

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.LGPL TODO
%attr(755,root,root) %{_bindir}/tp_tagger
%attr(755,root,root) %{_bindir}/trm
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%dir %{_libdir}/tunepimp
%dir %{_libdir}/tunepimp/plugins
%attr(755,root,root) %{_libdir}/tunepimp/plugins/*.tpp

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/tunepimp

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
