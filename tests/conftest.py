import pytest
import os

# Garante que os testes não toquem no CSV real
os.environ["CSV_FILENAME"] = "test_store.csv"
