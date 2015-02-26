%define api 5
%define major %api

%define api 5
%define qtminor 4
%define qtsubminor 1

%define qtversion %{api}.%{qtminor}.%{qtsubminor}

%define qtserialport %mklibname qt%{api}serialport %{major}
%define qtserialportd %mklibname qt%{api}serialport -d
%define qtserialport_p_d %mklibname qt%{api}serialport-private -d

%define qttarballdir qtserialport-opensource-src-%{qtversion}
%define _qt5_prefix %{_libdir}/qt%{api}

Name:		qt5-qtserialport
Version:	%{qtversion}
Release:	1
Summary:	Qt Location
Group:		Development/KDE and Qt
License:	LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
URL:		http://www.qt-project.org
Source0:	http://download.qt-project.org/official_releases/qt/%{api}.%{qtminor}/%{version}/submodules/%{qttarballdir}.tar.xz
BuildRequires:	qt5-qtbase-devel >= %{version}
BuildRequires:	pkgconfig(libudev)

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
%exclude %{_qt5_includedir}/QtSerialPort/%qtversion

#------------------------------------------------------------------------------

%package -n %{qtserialport_p_d}
Summary: Devel files needed to build apps based on QtSerialport
Group:    Development/KDE and Qt
Requires: %{qtserialportd} = %version
Provides: qt5-serialport-private-devel = %version

%description -n %{qtserialport_p_d}
Devel files needed to build apps based on QtSerialport.

%files -n %{qtserialport_p_d}
%{_qt5_includedir}/QtSerialPort/%qtversion
%{_qt5_prefix}/mkspecs/modules/qt_lib_serialport_private.pri

#------------------------------------------------------------------------------

%prep
%setup -q -n %qttarballdir

%build
%qmake_qt5
%make

#------------------------------------------------------------------------------
%install
%makeinstall_std INSTALL_ROOT=%{buildroot}

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
