from app.db import db
from app.db.models import User
import os 
import io

def test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data

def test_auth_pages(client):
    """This makes the index page"""
    response = client.get("/dashboard")
    assert response.status_code == 302
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200

def test_deny_access_dashboard_page_without_login(client):
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/login'
    html = response.get_data(as_text=True)
    assert 'Please log in to access this page.' in html

def test_deny_access_song_upload_page_without_login(client):
    response = client.get('/songs/upload', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/login'
    html = response.get_data(as_text=True)
    assert 'Please log in to access this page.' in html    

def test_register_user(client, application):
    response = client.post('/register', data={
        'email': 'test@mail.com',
        'password': '123456',
        'confirm': '123456'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/login'
    # check user save in db
    user = User.query.filter_by(email='test@mail.com').first()    
    assert user is not None
    assert user.email == 'test@mail.com'

def test_login_and_redirect_to_dashboard(client, application):
    # first register user before login
    response = client.post('/register', data={
        'email': 'test@mail.com',
        'password': '123456',
        'confirm': '123456'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/login'

    # login
    # login with newly regitered user
    response = client.post('/login', data={
        'email': 'test@mail.com',
        'password': '123456',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/dashboard'
    html = response.get_data(as_text=True)
    assert '<p>Welcome: test@mail.com</p>' in html

    # after login access dashboard page
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/dashboard'
    html = response.get_data(as_text=True)
    assert '<p>Welcome: test@mail.com</p>' in html


    

