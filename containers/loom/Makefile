.PHONY: build test
LOOM_PACKAGE ?= ../../../guild-ledger-loom/package
MANIFEST_DIGEST = a85d54356d04fbdcfd3caf90a12ff6de48571e7188d8e49093ab0697561212af
SOURCE_SNAPSHOT ?= ../../vendor/loom/loom-3f2817818c68.tar.gz
build:
	python3 -B prepare.py --snapshot "$(SOURCE_SNAPSHOT)" --package "$(LOOM_PACKAGE)" --manifest-digest $(MANIFEST_DIGEST)
	docker build -t guild-ledger-loom-mock:local .
test:
	python3 -B tests/source_snapshot.py
	python3 -B tests/pipeline.py
