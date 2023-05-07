def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--url', default='https://www.vdonate.ml')
    parser.addoption('--vnc', action='store_true')