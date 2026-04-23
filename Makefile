# Run
run:
	python main.py

menu:
	python menu.py

depends:
	pip install -r requirements.txt

dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Tests
test:
	python -m pytest tests/ -v

test-cov:
	python -m pytest tests/ -v --tb=short

test-model:
	python -m pytest tests/test_model.py -v

test-service:
	python -m pytest tests/test_store_service.py -v

test-api:
	python -m pytest tests/test_api.py -v