.DEFAULT_GOAL := help

# ── OS detection ──────────────────────────────────────────────────────────────
ifeq ($(OS),Windows_NT)
    SYS_PYTHON   := python
    VENV_PYTHON  := venv\Scripts\python.exe
    VENV_PIP     := venv\Scripts\pip.exe
    VENV_UVICORN := venv\Scripts\uvicorn.exe
    RMDIR        := rmdir /s /q
else
    SYS_PYTHON   := python3
    VENV_PYTHON  := venv/bin/python
    VENV_PIP     := venv/bin/pip
    VENV_UVICORN := venv/bin/uvicorn
    RMDIR        := rm -rf
endif

.PHONY: help install install-backend install-frontend run run-backend run-frontend test clean

# ── Help ──────────────────────────────────────────────────────────────────────
help:
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "  install            Install backend + frontend dependencies"
	@echo "  install-backend    Create venv and install Python packages"
	@echo "  install-frontend   Install Node packages"
	@echo "  run                Start backend and frontend concurrently"
	@echo "  run-backend        Start FastAPI server on port 8000"
	@echo "  run-frontend       Start Angular dev server"
	@echo "  test               Run pytest"
	@echo "  clean              Remove venv and node_modules"
	@echo ""

# ── Install ───────────────────────────────────────────────────────────────────
install: install-backend install-frontend

install-backend:
	cd backend && \
	$(SYS_PYTHON) -m venv venv && \
	$(VENV_PIP) install --upgrade pip && \
	$(VENV_PIP) install -r requirements.txt

install-frontend:
	cd frontend && npm install

# ── Run ───────────────────────────────────────────────────────────────────────
run-backend:
	cd backend && $(VENV_UVICORN) main:app --reload --host 127.0.0.1 --port 8000

run-frontend:
	cd frontend && npm start

run:
ifeq ($(OS),Windows_NT)
	start "Backend" cmd /c "cd /d backend && $(VENV_UVICORN) main:app --reload --host 127.0.0.1 --port 8000"
	cd frontend && npm start
else
	(cd backend && $(VENV_UVICORN) main:app --reload --host 127.0.0.1 --port 8000) & \
	(cd frontend && npm start); \
	wait
endif

# ── Test ──────────────────────────────────────────────────────────────────────
test:
	cd backend && $(VENV_PYTHON) -m pytest

# ── Clean ─────────────────────────────────────────────────────────────────────
clean:
ifeq ($(OS),Windows_NT)
	if exist backend\venv $(RMDIR) backend\venv
	if exist frontend\node_modules $(RMDIR) frontend\node_modules
else
	$(RMDIR) backend/venv frontend/node_modules
endif
