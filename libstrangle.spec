%global commit abc123def4567890abcdef1234567890abcdef12
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global git_date 20231014
%global tag 1.0.0

Name:           libstrangle
Version:        %{tag}
Release:        1.%{git_date}git%{shortcommit}%{?dist}
Summary:        Simple FPS Limiter

License:        GPLv3
URL:            https://gitlab.com/torkel104/libstrangle
Source0:        %{url}/-/archive/master/libstrangle-%{commit}.tar.gz

%if 0%{?fedora}
BuildRequires: gcc
BuildRequires: gcc-c++
%ifarch x86_64
BuildRequires: glibc-devel(x86-32)
BuildRequires: libgcc(x86-32)
BuildRequires: libstdc++-devel(x86-32)
%endif
%endif
%if 0%{?is_opensuse}
BuildRequires: gcc
BuildRequires: gcc-c++
%ifarch x86_64
BuildRequires: glibc-devel-32bit
BuildRequires: gcc-32bit
BuildRequires: gcc-c++-32bit
%endif
%endif

Requires: vulkan-loader

%description
libstrangle is a simple frame rate limiter for Linux.

%ifarch x86_64
Requires: libstrangle-libs64 = %{version}-%{release}
Recommends: libstrangle-libs32 = %{version}-%{release}
%endif
%ifarch i686
Requires: libstrangle-libs32 = %{version}-%{release}
%endif
%ifnarch x86_64 i686
Requires: libstrangle-libs = %{version}-%{release}
%endif

%prep
%autosetup -n libstrangle-master-%{commit}

%build
%ifarch x86_64 i686
%make_build 32-bit %{?_smp_mflags}
%make_build 64-bit %{?_smp_mflags}
%else
%make_build native %{?_smp_mflags}
%endif

%install
%make_install install-common
%ifarch x86_64 i686
    %make_install install-32
    %make_install install-64
    %ifarch x86_64
      echo "%{_libdir}/libstrangle/lib64/" > %{buildroot}/etc/ld.so.conf.d/libstrangle64.conf
    %endif
    %ifarch i686
      echo "%{_libdir}/libstrangle/lib32/" > %{buildroot}/etc/ld.so.conf.d/libstrangle32.conf
    %endif
%else
    # For non-x86 architectures, the project’s native target handles all installation.
    %make_install install-native
    echo "%{_libdir}" > %{buildroot}/etc/ld.so.conf.d/libstrangle.conf
%endif


%post -p %{_sbindir}/ldconfig
%postun -p %{_sbindir}/ldconfig

%files
%license libstrangle/LICENSE
%doc libstrangle/README.md
%{_bindir}/strangle
%{_bindir}/stranglevk
%{_datadir}/vulkan/implicit_layer.d/libstrangle_vk.json

%package libs32
Summary:       32-bit libstrangle libraries
Requires:      libstrangle = %{version}-%{release}
ExclusiveArch: %{ix86}

%description libs32
%summary

%files libs32
%{_libdir}/libstrangle/lib32/*.so
%{_sysconfdir}/ld.so.conf.d/libstrangle32.conf

%package libs64
Summary:       64-bit libstrangle libraries
Requires:      libstrangle = %{version}-%{release}
ExclusiveArch: x86_64

%description libs64
%summary

%files libs64
%{_libdir}/libstrangle/lib64/*.so
%{_sysconfdir}/ld.so.conf.d/libstrangle64.conf

%ifnarch x86_64 i686
%package libs
Summary:       libstrangle libraries
Requires:      libstrangle = %{version}-%{release}

%description libs
%summary

%files libs
%{_libdir}/libstrangle.so
%{_libdir}/libstrangle_nodlsym.so
%{_libdir}/libstrangle_vk.so
%{_sysconfdir}/ld.so.conf.d/libstrangle.conf
%endif

%changelog
%autochangelog
