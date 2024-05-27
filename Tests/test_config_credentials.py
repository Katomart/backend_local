import json
import pytest

def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

def test_config():
    config = load_config()
    assert 'platforms' in config, "Config file must include 'platforms'"
    for platform in config['platforms']:
        assert 'name' in platform, "Each platform must have a 'name'"
        assert 'enabled' in platform, "Each platform must have an 'enabled' flag"
        assert 'credentials' in platform, "Each platform must include 'credentials'"
        assert 'username' in platform['credentials'], "Credentials must include 'username'"
        assert 'password' in platform['credentials'], "Credentials must include 'password'"
