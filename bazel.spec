# they warn against fetching source ... but it's so convenient :-\

%define _disable_source_fetch 0

Name:           bazel
Version:        1.2.0
Release:        1%{?dist}
Summary:        Correct, reproducible, and fast builds for everyone.
License:        Apache License 2.0
URL:            http://bazel.io/
Source0:        https://github.com/bazelbuild/bazel/releases/download/%{version}/%{name}-%{version}-dist.zip

# remove once https://github.com/bazelbuild/bazel/issues/8666 (https://github.com/grpc/grpc/pull/18950) is resolved
Patch0:         https://patch-diff.githubusercontent.com/raw/grpc/grpc/pull/18950.patch
# FIXME: Java 11 log.warning generates backtrace
Patch1:         bazel-1.0.0-log-warning.patch

BuildRequires:  java-11-openjdk-devel
#BuildRequires:  java-1_8_0-openjdk-headless ## OpenSUSE
#BuildRequires:  java-1.8.0-openjdk-headless ## Mageia
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig(bash-completion)
BuildRequires:  findutils
BuildRequires:  gcc-c++
BuildRequires:  which
BuildRequires:  unzip
BuildRequires:  zip

# only for centos7/rhel7. rhel8 has `python3`.
%if 0%{?rhel} > 6 && 0%{?rhel} < 8
BuildRequires:  python
%else
BuildRequires:  python3
%endif

Requires:       java-11-openjdk-devel
#Requires:       java-1_8_0-openjdk-headless ## OpenSUSE
#Requires:       java-1.8.0-openjdk-headless ## Mageia

%define bashcompdir %(pkg-config --variable=completionsdir bash-completion 2>/dev/null)
%global debug_package %{nil}
%define __os_install_post %{nil}

%description
Correct, reproducible, and fast builds for everyone.

%prep
%setup -q -c -n %{name}-%{version}

pushd third_party/grpc/
%patch0 -p0
popd
%patch1 -p0


%build
%if 0%{?rhel} > 6 && 0%{?rhel} < 8
export EXTRA_BAZEL_ARGS="${EXTRA_BAZEL_ARGS} --host_force_python=PY2"
%else
# thanks to @aehlig for this tip: https://github.com/bazelbuild/bazel/issues/8665#issuecomment-503575270
find . -type f -regextype posix-extended -iregex '.*(sh|txt|py|_stub|stub_.*|bazel|get_workspace_status|protobuf_support|_so)' -exec %{__sed} -i -e '1s|^#!/usr/bin/env python$|#!/usr/bin/env python3|' "{}" \;
export EXTRA_BAZEL_ARGS="${EXTRA_BAZEL_ARGS} --python_path=/usr/bin/python3"

# horrible of horribles, just to have `python` in the PATH
# https://github.com/bazelbuild/bazel/issues/8665
%{__mkdir_p} ./bin-hack
%{__ln_s} /usr/bin/python3 ./bin-hack/python
export PATH=$(pwd)/bin-hack:$PATH
%endif

%ifarch aarch64
export EXTRA_BAZEL_ARGS="${EXTRA_BAZEL_ARGS} --nokeep_state_after_build --notrack_incremental_state --nokeep_state_after_build"
%else
%endif

%ifarch s390x
# increase heap size to addess s390x build failures
export BAZEL_JAVAC_OPTS="-J-Xmx4g -J-Xms512m"
%else
%endif

# loose epoch from their release date
export SOURCE_DATE_EPOCH="$(date -d $(head -1 CHANGELOG.md | %{__grep} -Eo '\b[[:digit:]]{4}-[[:digit:]]{2}-[[:digit:]]{2}\b' ) +%s)"
export EMBED_LABEL="%{version}"

# for debugging's sake
which g++
g++ --version

export TMPDIR=%{_tmppath}
export CC=gcc
export CXX=g++
export EXTRA_BAZEL_ARGS="${EXTRA_BAZEL_ARGS} --sandbox_debug --host_javabase=@local_jdk//:jdk --verbose_failures"
env ./compile.sh
%ifnarch ppc64le
env ./output/bazel build ${EXTRA_BAZEL_ARGS} //scripts:bazel-complete.bash
%endif
env ./output/bazel shutdown

%install
%{__mkdir_p} %{buildroot}/%{_bindir}
%{__mkdir_p} %{buildroot}/%{bashcompdir}
%{__cp} output/bazel %{buildroot}/%{_bindir}/bazel-real
%{__cp} ./scripts/packages/bazel.sh %{buildroot}/%{_bindir}/bazel
%ifnarch ppc64le
%{__cp} ./bazel-bin/scripts/bazel-complete.bash %{buildroot}/%{bashcompdir}/bazel
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/bazel
%attr(0755,root,root) %{_bindir}/bazel-real
%ifnarch ppc64le
%attr(0755,root,root) %{bashcompdir}/bazel
%endif


%changelog
* Wed Nov 18 2019 Vincent Batts <vbatts@fedoraproject.org> 1.2.0-1
- update to 1.2.0

* Mon Oct 21 2019 Vincent Batts <vbatts@fedoraproject.org> 1.1.0-1
- update to 1.1.0

* Wed Oct 16 2019 Vincent Batts <vbatts@fedoraproject.org> 1.0.0-1
- reconcile changes for multiarch

* Thu Oct 10 2019 Vincent Batts <vbatts@fedoraproject.org> 1.0.0-0
- update to 1.0.0

* Tue Sep 10 2019 Vincent Batts <vbatts@fedoraproject.org> 0.29.1-0
- update to 0.29.1

* Wed Aug 28 2019 Vincent Batts <vbatts@fedoraproject.org> 0.29.0-0
- update to 0.29.0

* Fri Jul 19 2019 Vincent Batts <vbatts@fedoraproject.org> 0.28.1-0
- update to 0.28.1

* Fri Jul 19 2019 Vincent Batts <vbatts@fedoraproject.org> 0.28.0-0
- update to 0.28.0

* Thu Jul 11 2019 Vincent Batts <vbatts@fedoraproject.org> 0.27.2-0
- update to 0.27.2

* Thu Jul 04 2019 Vincent Batts <vbatts@fedoraproject.org> 0.27.1-0
- update to 0.27.1

* Fri Jun 21 2019 Vincent Batts <vbatts@fedoraproject.org> 0.27.0-7
- carry patch for grpc fix due to newest glibc

* Thu Jun 20 2019 Kelvin Lu <kelvinlu@squareup.com> 0.27.0-6
- rename the real bazel binary as `bazel-real` and install the bash wrapper
  (`scripts/packages/bazel.sh`) in its place

* Thu Jun 20 2019 Vincent Batts <vbatts@fedoraproject.org> 0.27.0-5
- fixing the version output

* Wed Jun 19 2019 Vincent Batts <vbatts@fedoraproject.org> 0.27.0-4
- python3 workaround again, but for rhel8-beta as well

* Tue Jun 18 2019 Vincent Batts <vbatts@fedoraproject.org> 0.27.0-3
- python3 workaround for fedora's

* Mon Jun 17 2019 Vincent Batts <vbatts@fedoraproject.org> 0.27.0-2
- python3 everywhere

* Mon Jun 17 2019 Vincent Batts <vbatts@fedoraproject.org> 0.27.0-1
- update to 0.27.0

* Tue Jun 11 2019 Vincent Batts <vbatts@fedoraproject.org> 0.26.0-2
- update to 0.26.0

* Fri May 24 2019 Vincent Batts <vbatts@fedoraproject.org> 0.25.3-2
- trying aarch64 specific flags

* Fri May 24 2019 Vincent Batts <vbatts@fedoraproject.org> 0.25.3-1
- update to 0.25.3

* Mon May 13 2019 Vincent Batts <vbatts@fedoraproject.org> 0.25.2-1
- update to 0.25.2

* Mon May 13 2019 Vincent Batts <vbatts@fedoraproject.org> 0.25.1-1
- update to 0.25.1

* Mon May 13 2019 Vincent Batts <vbatts@fedoraproject.org> 0.25.0-3
- less janky use of python3

* Wed May 08 2019 Vincent Batts <vbatts@fedoraproject.org> 0.25.0-2
- actually use host jdk
- bazel didn't fully compile with openjdk 1.8.0, updated to 11

* Thu May 02 2019 Vincent Batts <vbatts@fedoraproject.org> 0.25.0-1
- update to 0.25.0
- https://github.com/bazelbuild/bazel/releases/tag/0.25.0

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
