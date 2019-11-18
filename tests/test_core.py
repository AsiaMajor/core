import pytest
import os
import sys
from server import init_app
from flask import Flask
from api.forms import ResponseForm
from modules import ping, preprocess

def test_core_init():
    '''test flask init'''
    #pass
    app = 0
    app = init_app()
    assert app!=0


def test_core_dbconn():
    pass

def test_core_apiresponse():
    #pass
    res = ResponseForm()
    res.result = ping.Controller().mock()
    assert res.result == "Pong!"
    assert res.success == True



