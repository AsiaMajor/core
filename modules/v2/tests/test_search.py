import pytest
from modules.v2.search import Search

def test_Search_init():
    search_agent = Search()
    assert search_agent
