
pkgname := bazel

pwd := $(shell pwd)

default: srpm

all: rpm srpm

rpm:
	rpmbuild \
                --define '_sourcedir $(pwd)' \
                --define '_specdir $(pwd)' \
                --define '_builddir $(pwd)' \
                --define '_srcrpmdir $(pwd)' \
                --define '_rpmdir $(pwd)' \
                --nodeps \
                -bb ./$(pkgname).spec

srpm: $(pkgname).spec $(wildcard *.diff)
	rpmbuild \
                --define '_sourcedir $(pwd)' \
                --define '_specdir $(pwd)' \
                --define '_builddir $(pwd)' \
                --define '_srcrpmdir $(pwd)' \
                --define '_rpmdir $(pwd)' \
                --nodeps \
                -bs ./$(pkgname).spec

clean:
	rm -rf *~ *.rpm noarch

