Summary:	The MusicBrainz tagging library
Summary(pl):	Biblioteka znakowania MusicBrainz
Name:		libtunepimp
Version:	0.2.0
Release:	1
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.musicbrainz.org/pub/musicbrainz/%{name}-%{version}.tar.gz
# Source0-md5:	fa80989ca4b164991866d314cb0b17ed
Patch0:		%{name}-readline.patch
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	libid3tag-devel >= 0.15.0b
BuildRequires:	libmad-devel
BuildRequires:	libmusicbrainz-devel >= 2.0.0
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
Summary(pl):	Pliki nag��wkowe biblioteki libtunepimp
Group:		Development/Libraries
Requires:	%{name} = %{version}
Requires:	libid3tag-devel
Requires:	libmad-devel
Requires:	libmusicbrainz-devel
Requires:	libvorbis-devel

%description devel
Header files for libtunepimp library.

%description devel -l pl
Pliki nag��wkowe biblioteki libtunepimp.

%package static
Summary:	Static libtunepimp library
Summary(pl):	Statyczna biblioteka libtunepimp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static libtunepimp library.

%description static -l pl
Statyczna biblioteka libtunepimp.

%prep
%setup -q
%patch -p1

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

# missing from make install
install -d $RPM_BUILD_ROOT%{_includedir}/tunepimp
install include/*.h lib/threads/posix/{mutex,thread,semaphore}.h \
	lib/{filecache,analyzer,submit,lookup,filelookup,write,trm,metadata,lookuptools}.h \
	$RPM_BUILD_ROOT%{_includedir}/tunepimp

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.LGPL TODO
%attr(755,root,root) %{_bindir}/tp_tagger
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/tunepimp

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
