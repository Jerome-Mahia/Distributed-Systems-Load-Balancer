.PHONY: build deploy

build:
	docker-compose build

deploy:
	docker-compose up -d


