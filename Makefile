test:
	python -m pytest tests/ -v
lint:
	python -m mypy src/jules/
typecheck:
	python -m mypy src/jules/
