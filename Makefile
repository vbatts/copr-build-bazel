pkgname		:= bazel
specname	?= $(pkgname).spec
pwd		:= $(shell pwd)
NAME		:= $(shell rpmspec -q --qf "%{name}" $(specname))
VERSION		:= $(shell rpmspec -q --qf "%{version}" $(specname))
RELEASE		:= $(shell rpmspec -q --qf "%{release}" $(specname))
NVR		:= $(NAME)-$(VERSION)-$(RELEASE)
outdir		?= $(pwd)

RELEASE_ID = $(shell grep '^ID=' /etc/*release | cut -d = -f 2 | tr -d \")
SUDO =

ifneq ($(shell id -u),0)
SUDO = sudo
endif

default: rpm

all: rpm srpm

name:
	@echo $(NVR)
	@echo "  NAME: $(NAME)"
	@echo "  VERSION: $(VERSION)"
	@echo "  RELEASE: $(RELEASE)"

rpm: .deps.$(RELEASE_ID) .builddep.$(RELEASE_ID)
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

$(NVR).src.rpm: .deps.$(RELEASE_ID) $(specname) $(wildcard *.diff)
	rpmbuild \
                --define '_sourcedir $(pwd)' \
                --define '_specdir $(pwd)' \
                --define '_builddir $(pwd)' \
                --define '_srcrpmdir $(outdir)' \
                --define '_rpmdir $(outdir)' \
                --nodeps \
                -bs ./$(specname)

.deps.$(RELEASE_ID):
ifeq ($(RELEASE_ID),centos)
	$(SUDO) yum install -y yum-utils rpm-build && touch $@
else
	$(SUDO) dnf install -y 'dnf-command(builddep)' rpm-build && touch $@
endif

.builddep.$(RELEASE_ID): $(specname)
ifeq ($(RELEASE_ID),centos)
	$(SUDO) yum-builddep -y $< && touch $@
else
	$(SUDO) dnf builddep -y $< && touch $@
endif

rebuild: .deps.$(RELEASE_ID) .builddep.$(RELEASE_ID) $(NVR).src.rpm
	rpmbuild --rebuild $(NVR).src.rpm

clean:
	rm -rf *~ *.rpm noarch .builddep.$(RELEASE_ID) .deps.$(RELEASE_ID) $(shell uname -m)/ $(NAME)-$(VERSION)/

