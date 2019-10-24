import pytest
from modules.ping import Ping
from modules.search import Search

def test_modules_ping_mock():
    ping_response = Ping().mock()
    assert ping_response == True