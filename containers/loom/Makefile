.PHONY: build test
LOOM_PACKAGE ?= ../../../guild-ledger-loom/package
MANIFEST_DIGEST = a85d54356d04fbdcfd3caf90a12ff6de48571e7188d8e49093ab0697561212af
build:
	test -n "$(LOOM_SOURCE)"
	python3 -B prepare.py --source "$(LOOM_SOURCE)" --package "$(LOOM_PACKAGE)" --manifest-digest $(MANIFEST_DIGEST)
	docker build -t guild-ledger-loom-mock:local .
test:
	python3 -B tests/pipeline.py
