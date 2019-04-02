# they warn against doing this ... :-\

%define _disable_source_fetch 0

Name:           bazel
Version:        0.24.1
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
BuildRequires:  which
Requires:       java-1.8.0-openjdk-devel

%define bashcompdir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null)
%global debug_package %{nil}
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
%{__mkdir_p} %{buildroot}/%{_bindir}
%{__mkdir_p} %{buildroot}/%{bashcompdir}
%{__cp} output/bazel %{buildroot}/%{_bindir}
%{__cp} ./bazel-bin/scripts/bazel-complete.bash %{buildroot}/%{bashcompdir}/bazel

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/bazel
%attr(0755,root,root) %{bashcompdir}/bazel


%changelog
* Tue Apr 02 2019 Vincent Batts <vbatts@fedoraproject.org> 0.24.2-1
- update to 0.24.1

* Tue Mar 26 2019 Vincent Batts <vbatts@fedoraproject.org> 0.24.0-1
- update to 0.24.0

* Mon Mar 11 2019 Vincent Batts <vbatts@fedoraproject.org> 0.23.2-1
- update to 0.23.2

* Mon Mar 04 2019 Vincent Batts <vbatts@fedoraproject.org> 0.23.1-1
- update to 0.23.1

* Tue Feb 26 2019 Vincent Batts <vbatts@fedoraproject.org> 0.23.0-1
- update to 0.23.0

* Tue Jan 29 2019 Vincent Batts <vbatts@fedoraproject.org> 0.22.0-1
- update to 0.22.0

* Wed Dec 19 2018 Vincent Batts <vbatts@fedoraproject.org> 0.21.0-1
- update to 0.21.0

* Mon Nov 19 2018 Vincent Batts <vbatts@fedoraproject.org> 0.19.2-1
- update to 0.19.2

* Mon Nov 12 2018 Vincent Batts <vbatts@fedoraproject.org> 0.19.1-1
- update to 0.19.1

* Tue Oct 30 2018 Vincent Batts <vbatts@fedoraproject.org> 0.19.0-2
- addressing https://github.com/bazelbuild/bazel/issues/6550

* Mon Oct 29 2018 Vincent Batts <vbatts@fedoraproject.org> 0.19.0-1
- update to 0.19.0

* Mon Oct 15 2018 Vincent Batts <vbatts@fedoraproject.org> 0.18.0-1
- update to 0.18.0

* Fri Sep 21 2018 Vincent Batts <vbatts@fedoraproject.org> 0.17.2-1
- update to 0.17.2

* Fri Sep 14 2018 Vincent Batts <vbatts@fedoraproject.org> 0.17.1-1
- update to 0.17.1

* Mon Aug 13 2018 Vincent Batts <vbatts@fedoraproject.org> 0.16.1-1
- update to 0.16.1

* Tue Jul 31 2018 Vincent Batts <vbatts@fedoraproject.org> 0.16.0-1
- update to 0.16.0

* Tue Jul 17 2018 Vincent Batts <vbatts@fedoraproject.org> 0.15.2-1
- update to 0.15.2

* Mon Jul 16 2018 Vincent Batts <vbatts@fedoraproject.org> 0.15.1-1
- update to 0.15.1

* Wed Jun 27 2018 Vincent Batts <vbatts@fedoraproject.org> 0.15.0-2
- add back the symbols (don't strip) as there is a binary embedded in the binary! :-O

* Tue Jun 26 2018 Vincent Batts <vbatts@fedoraproject.org> 0.15.0-1
- update to 0.15.0

* Fri Jun 22 2018 Vincent Batts <vbatts@fedoraproject.org> 0.14.1-2
- stripping the binary. 100.5Mb -> 1.5Mb. Could not isolate out the debuginfo
  into its own linked debuginfo package. Not sture whats going on there. But
  for now just stripping unneeded.

* Fri Jun 08 2018 Vincent Batts <vbatts@fedoraproject.org> 0.14.1-1
- update to 0.14.1

* Fri Jun 01 2018 Vincent Batts <vbatts@fedoraproject.org> 0.14.0-1
- update to 0.14.0

* Wed May 23 2018 Vincent Batts <vbatts@fedoraproject.org> 0.13.1-1
- update to 0.13.1

* Mon Apr 30 2018 Vincent Batts <vbatts@fedoraproject.org> 0.13.0-1
- update to 0.13.0

* Fri Apr 13 2018 Vincent Batts <vbatts@fedoraproject.org> 0.12.0-1
- update to 0.12.0

* Thu Feb 22 2018 Vincent Batts <vbatts@fedoraproject.org> 0.10.1-1
- update to 0.10.1

* Thu Feb 01 2018 Vincent Batts <vbatts@fedoraproject.org> 0.10.0-1
- update to 0.10.0

* Tue Jan 16 2018 Vincent Batts <vbatts@fedoraproject.org> 0.9.0-1
- update to 0.9.0

* Thu Nov 30 2017 Vincent Batts <vbatts@fedoraproject.org> 0.8.0-1
- update to 0.8.0

* Wed Oct 18 2017 Vincent Batts <vbatts@fedoraproject.org> 0.7.0-1
- update to 0.7.0

* Thu Sep 28 2017 Vincent Batts <vbatts@fedoraproject.org> 0.6.0-1
- update to 0.6.0

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
