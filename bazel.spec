# they warn against doing this ... :-\
%define _disable_source_fetch 0

Name:           bazel
Version:        0.5.4
Release:        1%{?dist}
Summary:        Correct, reproducible, and fast builds for everyone.
License:        Apache License 2.0
URL:            http://bazel.io/
Source0:        https://github.com/bazelbuild/bazel/releases/download/%{version}/%{name}-%{version}-dist.zip

BuildRequires:  java-1.8.0-openjdk-devel
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  python
BuildRequires:  gcc-c++
Requires:       java-1.8.0-openjdk-devel

%define bashcompdir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null)
%define debug_package %{nil}
%define __os_install_post %{nil}

%description
Correct, reproducible, and fast builds for everyone.

%prep
%setup -q -c -n %{name}-%{version}

%build
CC=gcc
CXX=g++
./compile.sh
./output/bazel build //scripts:bazel-complete.bash
./output/bazel shutdown

%install
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{bashcompdir}
cp output/bazel %{buildroot}/%{_bindir}
cp bazel-out/local-fastbuild/bin/scripts/bazel-complete.bash %{buildroot}/%{bashcompdir}/bazel

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/bazel
%attr(0755,root,root) %{bashcompdir}/bazel


%changelog
* Fri Aug 25 2017 Vincent Batts <vbatts@fedoraproject.org> 0.5.4-1
- adding missing builddeps

* Fri Aug 25 2017 Vincent Batts <vbatts@fedoraproject.org> 0.5.4-0
- update from upstream
- and spec cleanup for webhook builds

* Wed Aug 02 2017 Vincent Batts <vbatts@fedoraproject.org> 0.5.3-0
- update from upstream

* Wed Dec 21 2016 Byoungchan Lee <byoungchan.lee@gmx.com> 0.4.2-0
- update from upstream release

* Sun Dec 11 2016 Byoungchan Lee <byoungchan.lee@gmx.com> 0.3.2-0
- initial spec file 
