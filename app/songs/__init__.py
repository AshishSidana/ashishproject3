import csv
import logging
import os

from flask import Blueprint, render_template, abort, url_for,current_app
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.db import db
from app.db.models import Song
from app.songs.forms import csv_upload
from werkzeug.utils import secure_filename, redirect

songs = Blueprint('songs', __name__,
                        template_folder='templates')

@songs.route('/songs', methods=['GET'], defaults={"page": 1})
@songs.route('/songs/<int:page>', methods=['GET'])
def songs_browse(page):
    page = page
    per_page = 1000
    pagination = Song.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    try:
        return render_template('browse_songs.html',data=data,pagination=pagination)
    except TemplateNotFound:
        abort(404)

@songs.route('/songs/upload', methods=['POST', 'GET'])
@login_required
def songs_upload():
    form = csv_upload()
    if form.validate_on_submit():
        log = logging.getLogger("myApp")

        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        # log the song file
        log.info('Songs file uploaded filepath: '+ filepath)

        with open(filepath) as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:

                # user can upload same song one time, filter is based on song title & user_id
                song = Song.query.filter_by(title=row['Name'], user_id=current_user.id).first()
                if song is None:
                    current_user.songs.append(Song(row['Name'],row['Artist'],row['Year'],row['Genre'], current_user.id))
                    db.session.commit()

        return redirect(url_for('auth.dashboard'))

    try:
        return render_template('upload.html', form=form)
    except TemplateNotFound:
        abort(404)

@songs.route('/songs/delete', methods=['POST', 'GET'])
@login_required
def songs_delete():
    Song.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    log = logging.getLogger("myApp")
    log.info('My songs has been deleted')

    return redirect(url_for('auth.dashboard'))

@songs.route('/songs/deleteAll', methods=['POST', 'GET'])
@login_required
def songs_delete_all():
    db.session.query(Song).delete()
    db.session.commit()
    log = logging.getLogger("myApp")
    log.info('All songs has been deleted')

    return redirect(url_for('auth.dashboard'))