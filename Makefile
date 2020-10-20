pkgname		:= bazel
spec		?= $(pkgname).spec
pwd			:= $(shell pwd)
NAME		:= $(shell rpmspec -q --qf "%{name}" $(spec))
VERSION		:= $(shell rpmspec -q --qf "%{version}" $(spec))
RELEASE		:= $(shell rpmspec -q --qf "%{release}" $(spec))
NVR			:= $(NAME)-$(VERSION)-$(RELEASE)
outdir		?= $(pwd)

RELEASE_ID = $(shell grep '^ID=' /etc/*release | cut -d = -f 2 | tr -d \")
SUDO =

ifneq ($(shell id -u),0)
SUDO = sudo
endif

default: rpm

all: rpm srpm

version:
	@echo "v$(VERSION)-$(RELEASE)"

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
                -bb ./$(spec)

srpm: $(NVR).src.rpm

# https://developer.fedoraproject.org/deployment/copr/copr-cli.html
copr: $(NVR).src.rpm
	copr-cli build bazel $(NVR).src.rpm

$(NVR).src.rpm: .deps.$(RELEASE_ID) $(spec) $(wildcard *.diff)
	rpmbuild \
                --define '_sourcedir $(pwd)' \
                --define '_specdir $(pwd)' \
                --define '_builddir $(pwd)' \
                --define '_srcrpmdir $(outdir)' \
                --define '_rpmdir $(outdir)' \
                --nodeps \
                -bs ./$(spec)

.container: bazel.spec Makefile
	docker build -t bazel-build-v$(VERSION)-$(RELEASE) . && touch $@

.container.rebuild: .container
	docker run -it --rm -v $(HOME)/.config/copr:/root/.config/copr:ro bazel-build-v$(VERSION)-$(RELEASE) make rebuild && touch $@

.container.copr: .container
	docker run -it --rm -v $(HOME)/.config/copr:/root/.config/copr:ro bazel-build-v$(VERSION)-$(RELEASE) make copr && touch $@

.deps.$(RELEASE_ID):
ifeq ($(RELEASE_ID),centos)
	$(SUDO) yum install -y yum-utils rpm-build && touch $@
endif
ifeq ($(RELEASE_ID),pop)
	$(SUDO) dnf install -y 'dnf-command(builddep)' rpm-build && touch $@
endif
ifeq ($(RELEASE_ID),pop)
	$(SUDO) apt install -y 'rpm' && touch $@
endif
ifeq ($(RELEASE_ID),debian)
	$(SUDO) apt install -y 'rpm' && touch $@
endif
ifeq ($(RELEASE_ID),ubuntu)
	$(SUDO) apt install -y 'rpm' && touch $@
endif

.builddep.$(RELEASE_ID): $(spec)
ifeq ($(RELEASE_ID),centos)
	$(SUDO) yum-builddep -y $< && touch $@
else
	$(SUDO) dnf builddep -y $< && touch $@
endif

rebuild: .deps.$(RELEASE_ID) .builddep.$(RELEASE_ID) $(NVR).src.rpm
	rpmbuild --rebuild $(NVR).src.rpm

clean:
	rm -rf *~ *.rpm noarch .builddep.$(RELEASE_ID) .deps.$(RELEASE_ID) $(shell uname -m)/ $(NAME)-$(VERSION)/ .container*

