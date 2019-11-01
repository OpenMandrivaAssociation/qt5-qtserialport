%define api %(echo %{version} |cut -d. -f1)
%define major %api
%define beta beta2

%define qtserialport %mklibname qt%{api}serialport %{major}
%define qtserialportd %mklibname qt%{api}serialport -d
%define qtserialport_p_d %mklibname qt%{api}serialport-private -d

%define _qt5_prefix %{_libdir}/qt%{api}

Name:		qt5-qtserialport
Version:	5.14.0
%if "%{beta}" != ""
Release:	0.%{beta}.1
%define qttarballdir qtserialport-everywhere-src-%{version}-%{beta}
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/submodules/%{qttarballdir}.tar.xz
%else
Release:	1
%define qttarballdir qtserialport-everywhere-src-%{version}
Source0:	http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}.tar.xz
%endif
Source100:	%{name}.rpmlintrc
Summary:	Qt Location
Group:		Development/KDE and Qt
License:	LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
URL:		http://www.qt.io
BuildRequires:	qmake5 >= %{version}
BuildRequires:	pkgconfig(Qt5Core) >= %{version}
BuildRequires:	pkgconfig(Qt5Widgets) >= %{version}
BuildRequires:	pkgconfig(Qt5Test) >= %{version}
BuildRequires:	pkgconfig(libudev)
# For the Provides: generator
BuildRequires:	cmake >= 3.11.0-1

%description
Qt is a GUI software toolkit which simplifies the task of writing and
maintaining GUI (Graphical User Interface) applications for the X
Window System. Qt is written in C++ and is fully object-oriented.

#------------------------------------------------------------------------------

%package -n %{qtserialport}
Summary: Qt%{api} Component Library
Group: System/Libraries

%description -n %{qtserialport}
Qt%{api} Component Library.

Qt Serial Port provides the basic functionality, which includes configuring,
I/O operations, getting and setting the control signals of the RS-232 pinouts.

%files -n %{qtserialport}
%{_qt5_libdir}/libQt5SerialPort.so.%{api}*

#------------------------------------------------------------------------------

%package -n %{qtserialportd}
Summary: Devel files needed to build apps based on QtSerialport
Group: Development/KDE and Qt
Requires: %{qtserialport} = %version

%description -n %{qtserialportd}
Devel files needed to build apps based on Qt Serialport.

%files -n %{qtserialportd}
%{_qt5_libdir}/libQt5SerialPort.prl
%{_qt5_libdir}/libQt5SerialPort.so
%{_qt5_libdir}/pkgconfig/Qt5SerialPort.pc
%{_qt5_libdir}/cmake/Qt5SerialPort
%{_qt5_prefix}/mkspecs/modules/qt_lib_serialport.pri
%{_qt5_includedir}/QtSerialPort
%exclude %{_qt5_includedir}/QtSerialPort/%version

#------------------------------------------------------------------------------

%package -n %{qtserialport_p_d}
Summary: Devel files needed to build apps based on QtSerialport
Group:    Development/KDE and Qt
Requires: %{qtserialportd} = %version
Provides: qt5-serialport-private-devel = %version

%description -n %{qtserialport_p_d}
Devel files needed to build apps based on QtSerialport.

%files -n %{qtserialport_p_d}
%{_qt5_includedir}/QtSerialPort/%version
%{_qt5_prefix}/mkspecs/modules/qt_lib_serialport_private.pri

#------------------------------------------------------------------------------

%package examples
Summary: Examples for the Qt SerialPort library
Group: Development/KDE and Qt

%description examples
Examples for the Qt SerialPort library

%files examples
%{_qt5_prefix}/examples/*

#------------------------------------------------------------------------------

%prep
%autosetup -n %qttarballdir -p1

%build
%qmake_qt5
%make_build

#------------------------------------------------------------------------------
%install
%make_install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

# .la and .a files, die, die, die.
rm -f %{buildroot}%{_qt5_libdir}/lib*.la
