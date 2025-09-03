PROJECT_NAME=insider_automation
DOCKER_COMPOSE=docker-compose

.PHONY: build test clean shell logs

build:
	$(DOCKER_COMPOSE) build

test:
	$(DOCKER_COMPOSE) up --abort-on-container-exit --exit-code-from insider-tests

shell:
	$(DOCKER_COMPOSE) run --rm insider-tests bash

logs:
	$(DOCKER_COMPOSE) logs -f insider-tests

clean:
	rm -rf utils/screenshots/error_screenshots/* report.html test-results.xml .pytest_cache
