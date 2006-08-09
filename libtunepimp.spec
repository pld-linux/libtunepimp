Summary:	The MusicBrainz tagging library
Summary(pl):	Biblioteka znakowania MusicBrainz
Name:		libtunepimp
Version:	0.5.0
Release:	3
License:	GPL
Group:		Libraries
Source0:	ftp://ftp.musicbrainz.org/pub/musicbrainz/%{name}-%{version}.tar.gz
# Source0-md5:	2f303ff4fadcf51840e0f5e0e083d146
Patch0:		%{name}-ltdl.patch
Patch1:		%{name}-fix.patch
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	expat-devel
BuildRequires:	flac-devel
BuildRequires:	libltdl-devel
BuildRequires:	libmad-devel
BuildRequires:	libmusicbrainz-devel >= 2.1.0
BuildRequires:	libofa-devel >= 0.4.0
BuildRequires:	libstdc++-devel >= 2:1.4d
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	mpeg4ip-devel
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	taglib-devel >= 1.4
BuildRequires:	zlib-devel
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
Requires:	libltdl-devel
Requires:	libmusicbrainz-devel >= 2.1.0
Requires:	libstdc++-devel >= 2:1.4d

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

%package -n python-tunepimp
Summary:	Python bindings for libtunepimp library
Summary(pl):	Wi±zania Pythona do biblioteki libtunepimp
Group:		Libraries/Python
%pyrequires_eq	python-libs
Requires:	%{name} = %{version}-%{release}
Requires:	python-ctypes

%description -n python-tunepimp
Python bindings for libtunepimp library.

%description -n python-tunepimp -l pl
Wi±zania Pythona do biblioteki libtunepimp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

sed -i -e 's/ -O2//' configure.in

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

# perl bindings are not updated to current API
#cd perl/tunepimp-perl
#%{__perl} Makefile.PL \
#	OPTIMIZE="%{rpmcflags}"
#%{__make}
# cd ../..

cd python
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# not installed, but used by installed headers (track.h, tunepimp.h)
install lib/threads/posix/mutex.h \
	lib/{analyzer,filecache,plugins,readmeta,write}.h \
	include/tunepimp-*/metadata.h \
	$RPM_BUILD_ROOT%{_includedir}/tunepimp-0.5

rm -r $RPM_BUILD_ROOT%{_includedir}/tunepimp
ln -s tunepimp-0.5 $RPM_BUILD_ROOT%{_includedir}/tunepimp

#cd perl/tunepimp-perl
#%{__make} install \
#	DESTDIR=$RPM_BUILD_ROOT
#install -D examples/tp_tagger.pl $RPM_BUILD_ROOT%{_bindir}/tp_tagger
# cd ../..

cd python
python setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2
%py_postclean
install -D examples/trm.py $RPM_BUILD_ROOT%{_bindir}/trm

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.LGPL TODO
%attr(755,root,root) %{_bindir}/puid
%attr(755,root,root) %{_libdir}/libtunepimp.so.*.*.*
%dir %{_libdir}/tunepimp
%dir %{_libdir}/tunepimp/plugins
%attr(755,root,root) %{_libdir}/tunepimp/plugins/*.tpp

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtunepimp.so
%{_libdir}/libtunepimp.la
%{_includedir}/tunepimp
%{_includedir}/tunepimp-0.5

%files static
%defattr(644,root,root,755)
%{_libdir}/libtunepimp.a

%files -n python-tunepimp
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/trm
%dir %{py_sitescriptdir}/tunepimp
%{py_sitescriptdir}/tunepimp/*.py[co]
