%global debug_package %{nil}

%global commit 0273e318e3b0cc759155db8729ad74266b74cb9b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global git_date 20220222
%global tag 0.1.1

Name:           libstrangle
Version:        %{tag}
Release:        1.%{git_date}git%{shortcommit}%{?dist}
Summary:        Simple FPS Limiter

License:        GPLv3
URL:            https://gitlab.com/torkel104/libstrangle
Source0:        %{url}/-/archive/%{commit}/libstrangle-%{commit}.tar.gz

Patch0:         001-fix-build-gcc13.patch

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(x11)

Requires: vulkan-loader
Requires: libstrangle-libs = %{version}-%{release}

%ifarch x86_64
Recommends: libstrangle-libs(x86-32) = %{version}-%{release}
%endif

%description
libstrangle is a simple frame rate limiter for Linux.

%prep
%autosetup -n libstrangle-%{commit} -p1

%build
%make_build native %{?_smp_mflags}
echo "%{_libdir}/libstrangle" > %{_builddir}/libstrangle-%{commit}/libstrangle-%{_lib}.conf

%install
# Install common files (wrapper scripts, Vulkan layer JSON, and documentation)
install -m 0755 -D -T %{_builddir}/libstrangle-%{commit}/src/strangle.sh %{buildroot}%{_bindir}/strangle
install -m 0755 -D -T %{_builddir}/libstrangle-%{commit}/src/stranglevk.sh %{buildroot}%{_bindir}/stranglevk
install -m 0644 -D -T %{_builddir}/libstrangle-%{commit}/src/vulkan/libstrangle_vk.json %{buildroot}%{_datadir}/vulkan/implicit_layer.d/libstrangle_vk.json

# Install native target files
install -m 0755 -D -T %{_builddir}/libstrangle-%{commit}/build/libstrangle_native.so %{buildroot}%{_libdir}/libstrangle/libstrangle.so
install -m 0755 -D -T %{_builddir}/libstrangle-%{commit}/build/libstrangle_native_nodlsym.so %{buildroot}%{_libdir}/libstrangle/libstrangle_nodlsym.so
install -m 0755 -D -T %{_builddir}/libstrangle-%{commit}/build/libstrangle_vk_native.so %{buildroot}%{_libdir}/libstrangle/libstrangle_vk.so
install -m 0644 -D -T %{_builddir}/libstrangle-%{commit}/libstrangle-%{_lib}.conf %{buildroot}%{_sysconfdir}/ld.so.conf.d/libstrangle-%{_lib}.conf

%post -p %{_sbindir}/ldconfig
%postun -p %{_sbindir}/ldconfig

%files
%license COPYING
%doc README.md
%{_bindir}/strangle
%{_bindir}/stranglevk
%{_datadir}/vulkan/implicit_layer.d/libstrangle_vk.json

%package libs
Summary:       libstrangle libraries
%description libs
%summary

%files libs
%{_libdir}/libstrangle/libstrangle.so
%{_libdir}/libstrangle/libstrangle_nodlsym.so
%{_libdir}/libstrangle/libstrangle_vk.so
%{_sysconfdir}/ld.so.conf.d/libstrangle-%{_lib}.conf

%changelog
%autochangelog
