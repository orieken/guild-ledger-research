.PHONY: build test
build:
	docker build --target smoke -t guild-ledger-claude-smoke:local .
	docker build --target claude -t guild-ledger-claude:2.1.304 .
test:
	python3 -B tests/smoke.py
