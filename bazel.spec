# they warn against fetching source ... but it's so convenient :-\

%define _disable_source_fetch 0

Name:           bazel4
Version:        4.0.0
Release:        0%{?dist}
Summary:        Correct, reproducible, and fast builds for everyone.
License:        Apache License 2.0
URL:            http://bazel.io/
Source0:        https://github.com/bazelbuild/bazel/releases/download/%{version}/bazel-%{version}-dist.zip

# FIXME: Java 11 log.warning generates backtrace
Patch1:         bazel-1.0.0-log-warning.patch

# for folks with 'bazel' v1 package installed
Conflicts:      bazel
Conflicts:      bazel2

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
%setup -q -c -n bazel-%{version}

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
