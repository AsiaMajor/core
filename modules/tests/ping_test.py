import pytest
from modules.ping import Ping

def test_ping():
    ping_response = Ping().mock()
    assert ping_response == True