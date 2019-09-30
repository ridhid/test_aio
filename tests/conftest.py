import pytest

from tests.test_load import test_load


def pytest_configure(config):
    import sys

    sys._called_from_test = True


def pytest_unconfigure(config):
    import sys
    if hasattr(sys, "_called_from_test"):
        del sys._called_from_test


@pytest.fixture
async def load():
    await test_load()
