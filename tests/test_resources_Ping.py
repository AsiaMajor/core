import pytest
from modules.ping import Ping

def test_modules_ping_mock():
    ping_response = Ping().mock()
    assert ping_response == True