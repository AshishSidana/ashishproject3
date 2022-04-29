from app.db import db
from app.db.models import User
from app.db.models import Song
import os 
import io


def test_upload_csv(client, application):
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

    # access song upload page
    response = client.get('/songs/upload', follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/songs/upload'
    html = response.get_data(as_text=True)
    assert 'Upload Songs' in html
    
    # Read CSV file from system
    test_dir = os.path.join(os.getcwd(), 'tests') 
    with open(test_dir+"/music-test.csv") as f:
      file_content = f.read()

    # Submit CSV file POST call	
    file_name = "music.csv"
    data = {
        'file': (io.BytesIO(file_content.encode()), file_name)
    }
    response = client.post('/songs/upload', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == '/dashboard'

    # songs saved in db, 2 songs present in csv
    songs = Song.query.all()
    assert len(songs) == 2

    # file uploaded to uploads directory
    root = os.getcwd()
    upload_dir = os.path.join(os.getcwd(), 'uploads') 
    assert os.path.exists(upload_dir) == True
    assert os.path.exists(os.path.join(upload_dir, file_name)) == True
    

