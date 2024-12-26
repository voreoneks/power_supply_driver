SERVICES := app

help:
	@echo "Использование: make <command>"
	@echo "init                                 инициализация проекта"
	@echo "lint                                 запуск линтеров"
	@echo "test                                 запуск тестов"
	@echo "cover                                отчёт о покрытии тестами проекта"
	@echo "sort                                 сортировка импортов"

init:
	@poetry install
	@git-lfs install
	@git-lfs pull
	@pre-commit install

lint:
	@flake8 $(SERVICES)

test:
	@pytest

cover:
	@coverage run --concurrency=thread,greenlet --source=$(SERVICES) -m pytest tests
	@coverage report

sort:
	@isort . -m 3 -e --fgw -q
