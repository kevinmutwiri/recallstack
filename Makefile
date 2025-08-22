# Root Makefile for RecallStack

# Absolute path (from repo root)
VENV_DIR = backend/venv

# Path relative to inside backend/
VENV = venv

PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip

.PHONY: install lint format test clean venv backend frontend

venv:
	@test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r backend/requirements.txt
	cd frontend && npm install --legacy-peer-deps

lint: venv
	$(VENV_DIR)/bin/ruff check backend
	cd frontend && npm run lint

format: venv
	$(VENV_DIR)/bin/ruff format backend
	cd frontend && npx prettier --write .

test: venv
	$(VENV_DIR)/bin/pytest backend
	cd frontend && npm run test

clean:
	rm -rf $(VENV_DIR) backend/__pycache__ backend/.pytest_cache frontend/node_modules

# ---------- Run ----------
backend:
	cd backend && $(VENV)/bin/python manage.py runserver

frontend:
	cd frontend && npm run dev
