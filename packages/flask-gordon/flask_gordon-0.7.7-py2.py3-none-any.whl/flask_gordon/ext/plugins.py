from pytest import fixture


def _mock_current_settings(mocker):
    mock = mocker.patch("flask_gordon.ext.ctx._get_current_settings")
    mock.return_value = {}
    return mock


@fixture(name="current_settings", scope="function")
def mock_current_settings(mocker):
    yield _mock_current_settings(mocker)


@fixture(name="_current_settings", scope="function")
def mock_current__settings(mocker):
    yield _mock_current_settings(mocker)
