"""Root conftest.

Convention: no ``__init__.py`` anywhere in ``tests/``; pytest imports each test file by its
basename, so basenames must be unique across the tree. Run ``pytest`` from the repository root
so ``from src.xxx import yyy`` resolves; rootdir detection is left to pytest's defaults (no
pytest.ini).
"""
