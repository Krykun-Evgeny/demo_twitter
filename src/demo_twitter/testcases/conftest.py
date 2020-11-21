import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--cmd_opt_browser_name", action="store", default="chrome", help="Define a browser name: 'chrome', 'firefox'"
    )
    parser.addoption(
        "--cmd_opt_username_email", action="store", default="test@gmail.com",
        help="Set email of twitter credentials"
    )
    parser.addoption(
        "--cmd_opt_username", action="store", default="test",
        help="Set username of twitter credentials"
    )
    parser.addoption(
        "--cmd_opt_password", action="store", default="test", help="Set password of twitter credentials"
    )


@pytest.fixture
def cmd_opt_browser_name(request):
    return request.config.getoption("--cmd_opt_browser_name")


@pytest.fixture
def cmd_opt_username_email(request):
    return request.config.getoption("--cmd_opt_username_email")


@pytest.fixture
def cmd_opt_username(request):
    return request.config.getoption("--cmd_opt_username")


@pytest.fixture
def cmd_opt_password(request):
    return request.config.getoption("--cmd_opt_password")

