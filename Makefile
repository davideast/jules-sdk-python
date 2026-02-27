test:
	python -m pytest tests/ -v || [ $$? -eq 5 ]

lint:
	python -m mypy src/jules/

typecheck:
	python -m mypy src/jules/
