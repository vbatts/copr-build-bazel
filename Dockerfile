ARG fed_ver=latest
FROM fedora:$fed_ver
WORKDIR /build
RUN dnf install -y 'dnf-command(builddep)' rpm-build make copr-cli
ADD . /build
RUN make srpm
