pkgname		:= bazel
specname	?= $(pkgname).spec
pwd		:= $(shell pwd)
NAME		?= $(shell rpmspec -q --qf "%{name}" $(specname))
VERSION		?= $(shell rpmspec -q --qf "%{version}" $(specname))
RELEASE		?= $(shell rpmspec -q --qf "%{release}" $(specname))
NVR		:= $(NAME)-$(VERSION)-$(RELEASE)
outdir		?= $(pwd)

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

$(NVR).src.rpm: $(specname) $(wildcard *.diff)
	rpmbuild \
                --define '_sourcedir $(pwd)' \
                --define '_specdir $(pwd)' \
                --define '_builddir $(pwd)' \
                --define '_srcrpmdir $(outdir)' \
                --define '_rpmdir $(outdir)' \
                --nodeps \
                -bs ./$(specname)

builddep: $(NVR).src.rpm
	dnf builddep -y $<

rebuild: builddep
	rpmbuild --rebuild $(NVR).src.rpm

clean:
	rm -rf *~ *.rpm noarch

