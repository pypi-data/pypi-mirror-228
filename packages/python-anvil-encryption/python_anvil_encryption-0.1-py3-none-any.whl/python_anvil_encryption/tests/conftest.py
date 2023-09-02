"""Unit tests configuration file."""
import json
import os

import log
import pytest

FILE_DIR = os.path.dirname(os.path.realpath(__file__))


def pytest_configure(config):
    """Disable verbose output when running tests."""
    log.init(debug=True)

    terminal = config.pluginmanager.getplugin("terminal")
    terminal.TerminalReporter.showfspath = False


def _get_data_file(file_path, is_json=False):
    data = None
    with open(file_path, "rb") as json_file:
        if is_json:
            data = json.loads(json_file.read())
        else:
            data = json_file.read()
    return data


@pytest.fixture
def forge_complete_payload():
    return _get_data_file(
        os.path.join(FILE_DIR, "data", "aa_forge_complete_payload.json"), is_json=True
    )


@pytest.fixture
def private_key():
    return _get_data_file(os.path.join(FILE_DIR, "data", "aa.pem"))


@pytest.fixture
def public_key():
    return _get_data_file(os.path.join(FILE_DIR, "data", "aa.pub"))
