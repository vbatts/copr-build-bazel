
pkgname := bazel
specname ?= $(pkgname).spec
pwd := $(shell pwd)
NAME ?= $(shell rpmspec -q --qf "%{name}" $(specname))
VERSION ?= $(shell rpmspec -q --qf "%{version}" $(specname))
RELEASE ?= $(shell rpmspec -q --qf "%{release}" $(specname))
NVR := $(NAME)-$(VERSION)-$(RELEASE)

default: srpm

all: rpm srpm

name:
	@echo $(NVR)

rpm:
	rpmbuild \
                --define '_sourcedir $(pwd)' \
                --define '_specdir $(pwd)' \
                --define '_builddir $(pwd)' \
                --define '_srcrpmdir $(pwd)' \
                --define '_rpmdir $(pwd)' \
                -bb ./$(specname)

srpm: $(NVR).src.rpm

$(NVR).src.rpm: $(specname) $(wildcard *.diff)
	rpmbuild \
                --define '_sourcedir $(pwd)' \
                --define '_specdir $(pwd)' \
                --define '_builddir $(pwd)' \
                --define '_srcrpmdir $(pwd)' \
                --define '_rpmdir $(pwd)' \
                --nodeps \
                -bs ./$(specname)

builddep: $(NVR).src.rpm
	dnf builddep -y $<

rebuild: builddep
	rpmbuild --rebuild $(NVR).src.rpm

clean:
	rm -rf *~ *.rpm noarch

