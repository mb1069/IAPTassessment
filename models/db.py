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
                Field('name', type='string', required=True),
                Field('private', type='boolean', default=True),
                Field('created_on', 'datetime', readable=False, writable=False, default=request.now))

# Ensure [user_id, name] pairs are unique so that a user cannot have two boxes with the same
# name but two users can have a box with the same name
db.comicbox.name.requires = IS_NOT_IN_DB(db(db.comicbox.user_id == request.vars.user), 'comicbox.name')

# publisher table
db.define_table('publisher',
                Field('user_id', 'reference auth_user', required=True),
                Field('name', type='string', required=True))

# Ensure [user_id. name] pairs are unique to avoid users having multiple publishers with the same name
db.publisher.name.requires = IS_NOT_IN_DB(db(db.publisher.user_id == request.vars.user), 'publisher.name')

# comic table
db.define_table('comicbook',
                Field('box_id', 'reference comicbox', required=True),
                Field('title', type='string', required=True),
                Field('cover', type='upload', uploadfield=True, autodelete=True),
                Field('issue_number', type='integer'),
                Field('publisher', 'reference publisher'),
                Field('description', type='text'))

# writertable

db.define_table('writer',
                Field('user_id', 'reference auth_user', required=True, ondelete='CASCADE'),
                Field('name', type='string', required=True))

# Ensure [user_id. name] pairs are unique to avoid users having multiple writers with the same name
db.writer.name.requires = IS_NOT_IN_DB(db(db.writer.user_id == request.vars.user), 'writer.name')


# comic_writer table

db.define_table('comicWriter',
                Field('comicbook_id', 'reference comicbook', required=True, ondelete='CASCADE'),
                Field('writer_id', 'reference writer', required=True, ondelete='CASCADE'),
                primarykey=['comicbook_id', 'writer_id'])

# artist_table

db.define_table('artist',
                Field('user_id', 'reference auth_user', required=True),
                Field('name', type='string', required=True))

# Ensure [user_id. name] pairs are unique to avoid users having multiple writers with the same name
db.artist.name.requires = IS_NOT_IN_DB(db(db.artist.user_id == request.vars.user), 'artist.name')



# artist_writer table

db.define_table('comicArtist',
                Field('comicbook_id', 'reference comicbook', required=True, ondelete='CASCADE'),
                Field('artist_id', 'reference artist', required=True, ondelete='CASCADE'),
                primarykey=['comicbook_id', 'artist_id'])
