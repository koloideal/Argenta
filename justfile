set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]
set shell := ["bash", "-c"]

# Вывести список всех рецептов
default:
    @just --list

# Запустить тесты через pytest
tests:
    python -m pytest tests

# Запустить тесты с отчетом о покрытии
tests-cov:
    python -m pytest --cov=argenta tests

# Запустить тесты с отчетом о покрытии с html репортом
tests-cov-html:
    python -m pytest --cov=argenta tests --cov-report=html

# Отформатировать код (Ruff + isort)
format:
    python -m ruff format ./src
    python -m isort ./src

# Проверить типы через mypy (strict)
mypy:
    python -m mypy -p argenta --strict

# Проверить стиль через wemake-python-styleguide
wps:
    python -m flake8 --format=wemake ./src

# Запустить линтер Ruff
ruff:
    python -m ruff check ./src

