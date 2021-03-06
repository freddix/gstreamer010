%define		gst_major_ver	0.10

Summary:	GStreamer Streaming-media framework runtime
Name:		gstreamer010
Version:	0.10.36
Release:	8
License:	LGPL
Group:		Libraries
Source0:	http://gstreamer.freedesktop.org/src/gstreamer/gstreamer-%{version}.tar.xz
# Source0-md5:	15389c73e091b1dda915279c388b9cb2
Patch0:		%{name}-without_ps_pdf.patch
Patch1:		%{name}-eps.patch
Patch2:		%{name}-inspect-rpm-format.patch
Patch3:		%{name}-bison.patch
URL:		http://gstreamer.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	check-devel
BuildRequires:	flex
BuildRequires:	gettext-autopoint
BuildRequires:	glib-gio-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	nasm
BuildRequires:	perl-base
BuildRequires:	pkg-config
BuildRequires:	popt-devel
BuildRequires:	xmlto
Requires:	%{name}-libs = %{version}-%{release}
Provides:	gstreamer = %{version}-%{release}
Obsoletes:	gstreamer < %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		gstdatadir	%{_datadir}/gstreamer-%{gst_major_ver}
%define		gstlibdir	%{_libdir}/gstreamer-%{gst_major_ver}
%define		gstincludedir	%{_includedir}/gstreamer-%{gst_major_ver}

%description
GStreamer is a streaming-media framework, based on graphs of filters
which operate on media data. Applications using this library can do
anything from real-time sound processing to playing videos, and just
about anything else media-related. Its plugin-based architecture means
that new data types or processing capabilities can be added simply by
installing new plugins.

%package libs
Summary:	GStreamer libraries
Group:		Libraries
Provides:	gstreamer-libs = %{version}-%{release}
Obsoletes:	gstreamer-libs < %{version}-%{release}

%description libs
GStreamer libraries.

%package devel
Summary:	Include files for GStreamer streaming-media framework
Group:		Development/Libraries
Requires:	gstreamer = %{version}-%{release}
Provides:	gstreamer-devel = %{version}-%{release}
Obsoletes:	gstreamer-devel < %{version}-%{release}

%description devel
This package contains the includes files necessary to develop
applications and plugins for GStreamer.

%package apidocs
Summary:	GStreamer API documentation
Group:		Documentation
Requires:	gtk-doc-common
Provides:	gstreamer-apidocs = %{version}-%{release}
Obsoletes:	gstreamer-apidocs < %{version}-%{release}

%description apidocs
GStreamer API documentation.

%prep
%setup -qn gstreamer-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0

%build
%{__autopoint}
patch -p0 < common/gettext.patch
%{__libtoolize}
%{__aclocal} -I common/m4 -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-debug		\
	--disable-examples	\
	--disable-pspdf		\
	--disable-silent-rules	\
	--disable-static	\
	--disable-tests		\
	--enable-docbook	\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{gstdatadir}/presets,%{_docdir}/gstreamer-devel-%{version}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_docdir}/gstreamer-{%{gst_major_ver},%{version}}
mv $RPM_BUILD_ROOT%{_docdir}/gstreamer-%{version}/{manual,pwg} \
	$RPM_BUILD_ROOT%{_docdir}/gstreamer-devel-%{version}

%find_lang gstreamer --all-name --with-gnome

%{__rm} $RPM_BUILD_ROOT%{gstlibdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f gstreamer.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/gst-feedback
%attr(755,root,root) %{_bindir}/gst-feedback-%{gst_major_ver}
%attr(755,root,root) %{_bindir}/gst-inspect
%attr(755,root,root) %{_bindir}/gst-inspect-%{gst_major_ver}
%attr(755,root,root) %{_bindir}/gst-launch
%attr(755,root,root) %{_bindir}/gst-launch-%{gst_major_ver}
%attr(755,root,root) %{_bindir}/gst-typefind
%attr(755,root,root) %{_bindir}/gst-typefind-%{gst_major_ver}
%attr(755,root,root) %{_bindir}/gst-xmlinspect
%attr(755,root,root) %{_bindir}/gst-xmlinspect-%{gst_major_ver}
%attr(755,root,root) %{_bindir}/gst-xmllaunch
%attr(755,root,root) %{_bindir}/gst-xmllaunch-%{gst_major_ver}
%attr(755,root,root) %{gstlibdir}/gst-plugin-scanner
%attr(755,root,root) %{gstlibdir}/*.so

%{_mandir}/man1/*

%files libs
%defattr(644,root,root,755)
%dir %{gstdatadir}
%dir %{gstdatadir}/presets
%dir %{gstlibdir}
%attr(755,root,root) %ghost %{_libdir}/lib*-%{gst_major_ver}.so.?
%attr(755,root,root) %{_libdir}/lib*-%{gst_major_ver}.so.*.*.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*-%{gst_major_ver}.so
%{_aclocaldir}/gst-element-check-%{gst_major_ver}.m4
%{gstincludedir}
%{_pkgconfigdir}/*-%{gst_major_ver}.pc
%{_datadir}/gir-1.0/*.gir

%files apidocs
%defattr(644,root,root,755)
%{_docdir}/gstreamer-devel-%{version}
%{_gtkdocdir}/gstreamer-%{gst_major_ver}
%{_gtkdocdir}/gstreamer-libs-%{gst_major_ver}
%{_gtkdocdir}/gstreamer-plugins-%{gst_major_ver}

