.PHONY: up down reset test-visible test-startup test-web
up:
	docker compose up --build -d --wait
down:
	docker compose down --remove-orphans
reset:
	docker compose down --volumes --remove-orphans
	docker compose up --build -d --wait
test-startup:
	python3 -m unittest discover -s tests -p 'test_startup.py' -v
test-visible:
	python3 -m unittest discover -s tests -p 'test_*.py' -v
	$(MAKE) test-web
test-web:
	docker compose run --rm --no-deps web npm test -- --run
