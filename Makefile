#!/usr/bin/make -f

SHELL := /bin/bash


.PHONY: addons

release:
	git config --global user.email "bot@cerp.cloud"
	git config --global user.name "Cerpbot"
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
	mkdir -p tmp/cache/pip
	chmod 777 tmp/cache/pip
	mkdir extra-addons -p
	git clone https://github.com/clouderp/keychain2
	rm -rf extra-addons/keychain2
	cp -a keychain2/addons/keychain2 extra-addons
	git clone https://github.com/clouderp/cli_argparse
	rm -rf extra-addons/cli_argparse
	cp -a cli_argparse/addons/cli_argparse extra-addons
	mkdir coverage
	chmod 777 coverage

travis: testenv
	sudo chmod -R 777 tmp/cache
	mkdir -p tmp/cache/coverage
	if [ ! -f tmp/cache/coverage/codecov-env ]; then curl --retry 10 -s https://codecov.io/env > tmp/cache/coverage/codecov-env; fi
	if [ ! -f tmp/cache/coverage/codecov-env ]; then travis_terminate 1; fi
	if [ ! -f tmp/cache/coverage/codecov ]; then \
		curl --retry 10 -s https://codecov.io/bash > tmp/cache/coverage/codecov; \
		chmod +x tmp/cache/coverage/codecov; \
	fi
	if [ ! -f tmp/cache/coverage/codecov ]; then travis_terminate 1; fi
