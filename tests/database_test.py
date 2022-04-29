import pytest
import os 
from app import * 
from flask import current_app

def test_database_folder_created(client):
    root = os.getcwd()
    dbdir = os.path.join(root, 'database') 
    assert os.path.exists(dbdir) == True