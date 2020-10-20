FROM fedora
WORKDIR /build
RUN dnf install -y 'dnf-command(builddep)' rpm-build make
ADD . /build
RUN make srpm
