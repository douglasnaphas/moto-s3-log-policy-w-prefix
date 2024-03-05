VENV := venv

all: help

help:
	@echo "try: help, venv, install, test, run, clean"

$(VENV)/bin/activate:
	python3 -m venv $(VENV)

install:
	. $(VENV)/bin/activate; \
	./$(VENV)/bin/pip install .

venv: $(VENV)/bin/activate

test: venv clean
	. $(VENV)/bin/activate; \
	pytest -s test.py

clean:
	rm -fr build
	rm -fr dist
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' ! -name '*.un~' -exec rm -f {} \;

.PHONY: all help install venv test clean
