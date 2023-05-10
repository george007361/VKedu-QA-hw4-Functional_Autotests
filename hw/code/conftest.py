import pytest

def pytest_addoption(parser: pytest.Parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--url', default='https://www.vdonate.ml')
    parser.addoption('--vnc', action='store_true')
    parser.addoption('--selenoid', action='store_true')
