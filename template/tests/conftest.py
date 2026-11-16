"""Root conftest.

Convention: no ``__init__.py`` anywhere in ``tests/``; pytest imports each test file by its
basename, so basenames must be unique across the tree. Test files never import each other or a
``conftest.py``; shared setup is a fixture (a helper function is a fixture that returns it).
Run ``pytest`` from the repository root with the package installed (``pip install -e .``).
"""
