FROM fedora:34
WORKDIR /build
RUN dnf install -y 'dnf-command(builddep)' rpm-build make copr-cli
ADD . /build
RUN make srpm
