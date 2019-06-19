pkgname		:= bazel
specname	?= $(pkgname).spec
pwd		:= $(shell pwd)
NAME		?= $(shell rpmspec -q --qf "%{name}" $(specname))
VERSION		?= $(shell rpmspec -q --qf "%{version}" $(specname))
RELEASE		?= $(shell rpmspec -q --qf "%{release}" $(specname))
NVR		:= $(NAME)-$(VERSION)-$(RELEASE)
outdir		?= $(pwd)

RELEASE_ID = $(shell grep '^ID=' /etc/*release | cut -d = -f 2 | tr -d \")
SUDO =

ifneq ($(USER),root)
SUDO = sudo
endif

default: srpm

all: rpm srpm

name:
	@echo $(NVR)

rpm:
	rpmbuild \
                --define '_sourcedir $(pwd)' \
                --define '_specdir $(pwd)' \
                --define '_builddir $(pwd)' \
                --define '_srcrpmdir $(outdir)' \
                --define '_rpmdir $(outdir)' \
                -bb ./$(specname)

srpm: $(NVR).src.rpm

# https://developer.fedoraproject.org/deployment/copr/copr-cli.html
copr: $(NVR).src.rpm
	copr-cli build bazel $(NVR).src.rpm

$(NVR).src.rpm: .deps $(specname) $(wildcard *.diff)
	rpmbuild \
                --define '_sourcedir $(pwd)' \
                --define '_specdir $(pwd)' \
                --define '_builddir $(pwd)' \
                --define '_srcrpmdir $(outdir)' \
                --define '_rpmdir $(outdir)' \
                --nodeps \
                -bs ./$(specname)

.deps:
ifeq ($(RELEASE_ID),centos)
	$(SUDO) yum install -y yum-utils rpm-build && touch $@
else
	$(SUDO) dnf install -y 'dnf-command(builddep)' rpm-build && touch $@
endif

.builddep: $(NVR).src.rpm
ifeq ($(RELEASE_ID),centos)
	$(SUDO) yum-builddep -y $< && touch $@
else
	$(SUDO) dnf builddep -y $< && touch $@
endif

rebuild: .deps .builddep
	rpmbuild --rebuild $(NVR).src.rpm

clean:
	rm -rf *~ *.rpm noarch .builddep .deps

