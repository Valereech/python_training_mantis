"""Module providing create and finalize fixture"""
import pytest
import json
import os.path
from fixture.application import Application


fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as cf:
            target = json.load(cf)
    return target


@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))['app_link']
    app_creds = load_config(request.config.getoption("--target"))['app_creds']
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config['baseUrl'])
    fixture.session.enshure_login(username=app_creds['username'], password=app_creds['password'])
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def the_end():
        fixture.session.enshure_logout()
        fixture.destroy()
    request.addfinalizer(the_end)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
