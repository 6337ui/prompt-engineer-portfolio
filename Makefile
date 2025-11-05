.PHONY: up down build demo

up:
	docker-compose up --build

down:
	docker-compose down

build:
	docker-compose build

demo:
	python3 trace-eval/harness.py