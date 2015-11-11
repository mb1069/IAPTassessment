# -*- coding: utf-8 -*-

#####################################
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
#####################################

# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# request.requires_https()

# app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
# once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
# choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


# (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
# (optional) static assets folder versioning
# response.static_version = '0.0.0'
#####################################
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
#####################################

from gluon.tools import Auth, Service, PluginManager

# if NOT running on Google App Engine use SQLite or other DB
db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])

auth = Auth(db)
# create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)

service = Service()
plugins = PluginManager()

# configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

# configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#####################################
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable',Field('myfield','string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
#####################################

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)


# comicbox table
# privacy field (if true private, else public)
db.define_table('comicbox',
                Field('user_id', 'reference auth_user', required=True),
                Field('box_name', type='string', required=True),
                Field('private', type='boolean', default=True),
                Field('created_on', 'datetime', readable=False, writable=False, default=request.now))

# Before callback to ensure [user_id, box_name] pairs are unique so that a user cannot have two boxes with the same 
# name but two users can have a box with the same name
db.comicbox._before_insert.append(
    lambda r: db((db.comicbox.user_id == r["user_id"]) & (db.comicbox.box_name == r["box_name"])).select())

# comic table
db.define_table('comicbook',
                Field('box_id', db.comicbox, required=True),
                Field('title', type='string', required=True),
                Field('cover', type='upload', uploadfield=True, uploadseparate=True, autodelete=True),
                Field('issue_number', type='integer'),
                Field('publisher', type='string'),
                Field('description', type='text'))

# writer_table

db.define_table('writer',
                Field('user_id', 'reference auth_user', required=True),
                Field('name', type='string', required=True))

# comic_writer table

db.define_table('comicWriter',
                Field('comicbook', 'reference comicbook', required=True),
                Field('writer', 'reference writer', required=True),
                primarykey=['comicbook', 'writer'])

# artist_table

db.define_table('artist',
                Field('user_id', 'reference auth_user', required=True),
                Field('name', type='string', required=True))


# artist_writer table

db.define_table('comicArtist',
                Field('comicbook', 'reference comicbook', required=True),
                Field('artist', 'reference artist', required=True),
                primarykey=['comicbook', 'artist'])

import os

db.comicbox.truncate()
db.comicbook.truncate()
if db(db.comicbox.id > -1).count() == 0:

    db.comicbox.truncate()
    db.comicbox.insert(user_id=1, box_name='Box A', private=True)
    db.comicbox.insert(user_id=1, box_name='Box B', private=True)
    db.comicbox.insert(user_id=1, box_name='Box C', private=True)
    db.comicbox.insert(user_id=1, box_name='Box D', private=True)
    db.comicbox.insert(user_id=1, box_name='Box E', private=True)
    db.comicbox.insert(user_id=1, box_name='Box F', private=True)

    db.comicbook.truncate()

    cover_path = os.path.join(os.path.dirname(__file__), '../static/images/superman.jpg')

    db.comicbook.insert(box_id=1, title='Superman1', publisher='DC', cover=open(cover_path))
    db.comicbook.insert(box_id=2, title='Superman2', publisher='Marvel', cover=open(cover_path))
    db.comicbook.insert(box_id=2, title='Superman2', cover=open(cover_path))
    db.comicbook.insert(box_id=3, title='Superman3', cover=open(cover_path))
    db.comicbook.insert(box_id=3, title='Superman3', cover=open(cover_path))
    db.comicbook.insert(box_id=3, title='Superman3', cover=open(cover_path))
    db.comicbook.insert(box_id=4, title='Superman4', cover=open(cover_path))
    db.comicbook.insert(box_id=4, title='Superman4', cover=open(cover_path))
    db.comicbook.insert(box_id=4, title='Superman4', cover=open(cover_path))
    db.comicbook.insert(box_id=4, title='Superman4', cover=open(cover_path))
    db.comicbook.insert(box_id=5, title='Superman5', cover=open(cover_path))
    db.comicbook.insert(box_id=5, title='Superman5', cover=open(cover_path))
    db.comicbook.insert(box_id=5, title='Superman5', cover=open(cover_path))
    db.comicbook.insert(box_id=5, title='Superman5', cover=open(cover_path))
    db.comicbook.insert(box_id=5, title='Superman5', cover=open(cover_path))
    db.comicbook.insert(box_id=5, title='Superman5', cover=open(cover_path))

    db.artist.truncate()
    db.writer.truncate()
    db.comicWriter.truncate()
    db.comicArtist.truncate()

    db.artist.insert(user_id=1, name='Artsy')
    db.artist.insert(user_id=1, name='Art')
    db.comicArtist.insert(comicbook=2, artist=1)
    db.comicArtist.insert(comicbook=2, artist=2)
    db.writer.insert(user_id=1, name='Writsy')
    db.writer.insert(user_id=1, name='Writ')
    db.comicWriter.insert(comicbook=1, writer=1)
    db.comicWriter.insert(comicbook=1, writer=2)
