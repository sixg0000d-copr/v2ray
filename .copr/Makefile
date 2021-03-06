MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
PROJECT_ROOT := $(abspath $(MAKEFILE_DIR)/..)

spec ?= $(PROJECT_ROOT)/v2ray-core.spec
outdir ?= $(PROJECT_ROOT)/outdir
source0 = $(shell spectool -s 0 $(spec) | awk '/Source0:/ { print $$2 }')
name-version = $(shell basename -s .tar.gz $(source0))

all: srpm

$(outdir):
	[ -d "$(outdir)" ] || mkdir -p $(outdir)

ifeq ($(shell id -u),0)
init:
	dnf -y install git golang rpmdevtools
else
init:
	sudo dnf -y install git golang rpmdevtools
endif

.ONESHELL:
source: init $(outdir)
	cd $(outdir)
	spectool -g -s 0 $(spec)
	tar xzf $(name-version).tar.gz
	cd $(name-version)
	go mod vendor
	tar czf ../$(name-version)-vendor.tar.gz vendor
	cd ..

	# Miscellaneous
	rm -rf $(outdir)/$(name-version)
	cp $(PROJECT_ROOT)/sources/* $(outdir)
	cp $(spec) $(outdir)

srpm: $(outdir) $(spec) source
	rpmbuild \
	--define "_sourcedir $(outdir)" \
	--define "_srcrpmdir $(outdir)" \
	-bs $(spec)

rpm: $(outdir) $(spec) source
	rpmbuild \
	--define "_sourcedir $(outdir)" \
	--define "_rpmdir $(outdir)" \
	-bb $(spec)

clean:
	rm -rf $(outdir)

.PHONY: all init source srpm rpm clean
