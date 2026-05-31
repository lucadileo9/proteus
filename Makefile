# Variables
PYTHON = python
PIP = $(PYTHON) -m pip
PYTEST = $(PYTHON) -m pytest
RUFF = ruff
MYPY = mypy
TOX = tox

.PHONY: help install install-dev test lint format typecheck all build clean tox

help:
	@echo "Disponibili i seguenti comandi:"
	@echo "  install      : Installa le dipendenze di runtime"
	@echo "  install-dev  : Installa le dipendenze di sviluppo e pre-commit"
	@echo "  test         : Esegue i test con copertura"
	@echo "  lint         : Controlla lo stile del codice (Ruff)"
	@echo "  format       : Formatta il codice (Ruff format)"
	@echo "  typecheck    : Controlla i tipi (Mypy)"
	@echo "  tox          : Esegue i test su tutte le versioni di Python supportate"
	@echo "  all          : Esegue format, lint, typecheck e test"
	@echo "  build        : Crea i file per la distribuzione (wheel/sdist)"
	@echo "  clean        : Rimuove file temporanei e cache"

install:
	$(PIP) install .

install-dev:
	$(PIP) install -e ".[dev]"
	pre-commit install

test:
	$(PYTEST) --cov=src/proteus --cov-report=term-missing

lint:
	$(RUFF) check src/ tests/

format:
	$(RUFF) check --fix src/ tests/
	$(RUFF) format src/ tests/

typecheck:
	$(MYPY) src/proteus/

tox:
	$(TOX)

all: format lint typecheck test

build:
	$(PIP) install build
	$(PYTHON) -m build

clean:
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('.pytest_cache')]"
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('.mypy_cache')]"
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('.tox')]"
	$(PYTHON) -c "import pathlib, os; [os.remove(p) for p in pathlib.Path('.').rglob('.coverage')]"
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('dist')]"
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('build')]"
