#!/usr/bin/make -f

SHELL := /bin/bash


.PHONY: addons

release:
	./scripts/release

icons:
	./scripts/icons

addons:
	./scripts/addons

devenv:
	docker build \
		--build-arg ODOO_VERSION=$$ODOO_VERSION \
		-t cerp/odoo:cerp-$$ODOO_VERSION \
		context

testenv:
	mkdir extra-addons -p
	git clone https://github.com/clouderp/keychain2
	rm -rf extra-addons/keychain2
	cp -a keychain2/addons/keychain2 extra-addons
	git clone https://github.com/clouderp/cli_argparse
	rm -rf extra-addons/cli_argparse
	cp -a cli_argparse/addons/cli_argparse extra-addons
	mkdir coverage
	chmod 777 coverage
