import pytest
import os 
from app import * 
from flask import current_app

def test_errors_log_file_created(client):
    root = os.getcwd()
    logdir = os.path.join(root, 'logs') 
    assert os.path.exists(logdir) == True
    assert os.path.exists(os.path.join(logdir, 'errors.log')) == True 

def test_handler_log_file_created(client):
    root = os.getcwd()
    logdir = os.path.join(root, 'logs') 
    assert os.path.exists(logdir) == True
    assert os.path.exists(os.path.join(logdir, 'handler.log')) == True 

def test_myapp_log_file_created(client):
    root = os.getcwd()
    logdir = os.path.join(root, 'logs') 
    assert os.path.exists(logdir) == True
    assert os.path.exists(os.path.join(logdir, 'myapp.log')) == True 

def test_request_log_file_created(client):
    root = os.getcwd()
    logdir = os.path.join(root, 'logs') 
    assert os.path.exists(logdir) == True
    assert os.path.exists(os.path.join(logdir, 'request.log')) == True 

def test_sqlalchemy_log_file_created(client):
    root = os.getcwd()
    logdir = os.path.join(root, 'logs') 
    assert os.path.exists(logdir) == True
    assert os.path.exists(os.path.join(logdir, 'sqlalchemy.log')) == True 

def test_werkzeug_log_file_created(client):
    root = os.getcwd()
    logdir = os.path.join(root, 'logs') 
    assert os.path.exists(logdir) == True
    assert os.path.exists(os.path.join(logdir, 'werkzeug.log')) == True 