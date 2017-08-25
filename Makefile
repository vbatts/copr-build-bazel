
pkgname := bazel
specname ?= $(pkgname).spec
pwd := $(shell pwd)
NAME ?= $(shell rpmspec -q --qf "%{name}" $(specname))
VERSION ?= $(shell rpmspec -q --qf "%{version}" $(specname))
RELEASE ?= $(shell rpmspec -q --qf "%{release}" $(specname))

default: srpm

all: rpm srpm

name:
	@echo $(NAME)-$(VERSION)-$(RELEASE)

rpm:
	rpmbuild \
                --define '_sourcedir $(pwd)' \
                --define '_specdir $(pwd)' \
                --define '_builddir $(pwd)' \
                --define '_srcrpmdir $(pwd)' \
                --define '_rpmdir $(pwd)' \
                -bb ./$(specname)

srpm: $(specname) $(wildcard *.diff)
	rpmbuild \
                --define '_sourcedir $(pwd)' \
                --define '_specdir $(pwd)' \
                --define '_builddir $(pwd)' \
                --define '_srcrpmdir $(pwd)' \
                --define '_rpmdir $(pwd)' \
                --nodeps \
                -bs ./$(specname)

clean:
	rm -rf *~ *.rpm noarch

