FROM fedora
WORKDIR /build
RUN dnf install -y 'dnf-command(builddep)' rpm-build java-1.8.0-openjdk-devel zlib-devel pkgconfig python gcc-c++ make
ADD . /build
RUN dnf builddep -y ./bazel.spec && make rpm
