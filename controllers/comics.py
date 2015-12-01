# Exam Candidate Number Y0076159


import helper
import os


def mycomics():
    items_per_page = 17

    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    if len(request.args) == 2:
        numitems = int(request.args[1])
    else:
        numitems = db((auth.user_id == db.comicbox.user_id) &
                     (db.comicbox.id == db.comicbook.box_id)).count()

    user_comics = db((auth.user_id == db.comicbox.user_id) &
                     (db.comicbox.id == db.comicbook.box_id)).select(db.comicbook.id, db.comicbox.id,
                                                                     db.comicbox.name, db.comicbook.title, db.comicbox.user_id,
                                                                     db.comicbook.cover, db.comicbook.issue_number,
                                                                     db.comicbook.publisher, db.comicbook.description,
                                                                     limitby=(page * items_per_page,
                                                                              (page + 1) * items_per_page))

    user_comics_id = []
    for row in user_comics:
        user_comics_id.append(row.comicbook.id)

    artist_comics = db(
        (db.artist.id == db.comicArtist.artist_id) & (db.comicArtist.comicbook_id.belongs(user_comics_id))).select(
        db.comicArtist.comicbook_id, db.artist.name)
    writer_comics = db(
        (db.writer.id == db.comicWriter.writer_id) & (db.comicWriter.comicbook_id.belongs(user_comics_id))).select(
        db.comicWriter.comicbook_id, db.writer.name)

    return {'user_comics': user_comics, 'artist_comics': artist_comics, 'writer_comics': writer_comics, 'page': page,
            'display_next': numitems>(page+1)*items_per_page}
    # return {'user_comics': user_comics}


def comicview():
    # Verify comicbookid exists
    if request.vars.comicbookid is None:
        redirect(URL('default', 'error', vars={
            'errormsg': 'Error: invalid data id:' + request.vars.comicbookid}))

    if len(db(db.comicbook.id == request.vars.comicbookid).select(db.comicbook.id)) == 0:
        redirect(URL('default', 'error', vars={
            'errormsg': 'Error: data id does not exist in database'}))

    left_joins = [db.comicWriter.on(db.comicWriter.comicbook_id == db.comicbook.id),
                  db.writer.on(db.comicWriter.writer_id == db.writer.id),
                  db.comicArtist.on(db.comicArtist.comicbook_id == db.comicbook.id),
                  db.artist.on(db.comicArtist.artist_id == db.artist.id),
                  db.publisher.on(db.comicbook.publisher == db.publisher.id)]

    comic_details = db((db.comicbook.id == request.vars.comicbookid) & (db.comicbook.box_id == db.comicbox.id)).select(
        db.comicbook.title,
        db.comicbook.issue_number,
        db.comicbox.user_id,
        db.comicbox.name,
        db.comicbook.description,
        db.artist.name, db.writer.name,
        db.comicbook.cover, db.publisher.name,
        left=left_joins)
    data = comic_details[0]
    comics_writers = db((db.comicWriter.comicbook_id == request.vars.comicbookid) &
                        (db.comicWriter.writer_id == db.writer.id)).select(db.writer.name).column()
    comics_artists = db((db.comicArtist.comicbook_id == request.vars.comicbookid) &
                        (db.comicArtist.artist_id == db.artist.id)).select(db.artist.name).column()
    return {'comicbookid': request.vars.comicbookid,
            'box_name': data.comicbox.name,
            'title': data.comicbook.title,
            'cover': data.comicbook.cover,
            'issue_number': data.comicbook.issue_number,
            'writers': comics_writers,
            'artists': comics_artists,
            'description': data.comicbook.description,
            'publisher': data.publisher.name,
            'owns_comic': data.comicbox.user_id == auth.user_id}


def comiccreate():
    # Verify comicbookid exists
    if auth.user_id is None:
        redirect(URL('default', 'error', vars={
            'errormsg': 'An error has occured: user is not logged in. Please login or create an account using the menu in the top right.'}))

    comicdata = {}
    if request.vars.comicbookid is not None:
        comicdata = comicview()

    defaultTitle = comicdata.get('title', '')
    # todo Copy cover from other comicbook
    # defaultCover = comicdata.get('cover', '')
    # As copied from other user, current user cannot be guaranteed to have same box
    defaultBoxName = 'Unfiled'
    defaultArtists = comicdata.get('artists', [])
    defaultWriters = comicdata.get('writers', [])
    defaultPublisher = comicdata.get('publisher', '')
    defaultIssue_number = comicdata.get('issue_number', '')
    defaultDescription = comicdata.get('description', '')

    if request.vars.boxid is not None:
        defaultBoxName = db(db.comicbox.id == request.vars.boxid).select(db.comicbox.name).column()[0]

    user_boxes = db(auth.user_id == db.comicbox.user_id).select(db.comicbox.name).column()
    if defaultBoxName not in user_boxes:
        defaultBoxName = user_boxes[0]

    form = SQLFORM.factory(
        Field('title', type='string', default=defaultTitle, required=True, requires=IS_NOT_EMPTY()),
        Field('box_name', type='string', default=defaultBoxName, required=True,
              requires=IS_IN_SET(user_boxes, zero=None)),
        Field('cover', type='upload', label='Cover max 400h * 300w px', uploadfolder=os.path.join(request.folder,'uploads'), requires=IS_EMPTY_OR(IS_IMAGE(maxsize=(300,400)))),
        Field('remove_existing_cover', type='boolean', label='Remove existing cover (automatic if cover uploaded above)', default=False),
        Field('artists', type='list:string', default=defaultArtists, requires=IS_NOT_EMPTY()),
        Field('writers', type='list:string', default=defaultWriters, requires=IS_NOT_EMPTY()),
        Field('issue_number', type='string', default=defaultIssue_number),
        Field('description', type='text', default=defaultDescription),
        table_name='comicbook', upload=URL('uploads'))

    if form.process().accepted:
        submit_comiccreate_form(form, db, request, auth)
        session.flash = 'Created comic!'
        redirect(URL('comics', 'mycomics'))

    return {'form': form}


def comicedit():
    # Verify comicbookid exists
    if request.vars.comicbookid is None:
        redirect(URL('default', 'error', vars={
            'errormsg': 'Error: invalid comicbook id:' + request.vars.comicbookid}))

    if len(db(db.comicbook.id == request.vars.comicbookid).select(db.comicbook.id)) == 0:
        redirect(URL('default', 'error', vars={
            'errormsg': 'Error: comicbook id does not exist in database'}))

    user_boxes = db(auth.user_id == db.comicbox.user_id).select(db.comicbox.name).column()

    # Verify user owns comicbook
    if len(db((db.comicbox.user_id == auth.user_id) & (db.comicbook.id == request.vars.comicbookid)
                      & (db.comicbook.box_id == db.comicbox.id)).select()) == 0:
        redirect(URL('default', 'error', vars={
            'errormsg': 'An error has occured: attempting to edit another user\'s comic'}))

    left_joins = [db.comicWriter.on(db.comicWriter.comicbook_id == db.comicbook.id),
                  db.writer.on(db.comicWriter.writer_id == db.writer.id),
                  db.comicArtist.on(db.comicArtist.comicbook_id == db.comicbook.id),
                  db.artist.on(db.comicArtist.artist_id == db.artist.id),
                  db.publisher.on(db.comicbook.publisher == db.publisher.id)]

    comic_details = db((db.comicbook.id == request.vars.comicbookid) & (db.comicbook.box_id == db.comicbox.id)).select(
        db.comicbook.title, db.comicbook.id,
        db.comicbook.cover,
        db.comicbook.issue_number,
        db.comicbox.name,
        db.comicbook.description,
        db.artist.name, db.writer.name,
        db.comicbook.cover, db.publisher.name,
        left=left_joins)
    comicbook = comic_details[0].comicbook
    comics_writers = db((db.comicWriter.comicbook_id == request.vars.comicbookid) &
                        (db.comicWriter.writer_id == db.writer.id)).select(db.writer.name).column()
    comics_artists = db((db.comicArtist.comicbook_id == request.vars.comicbookid) &
                        (db.comicArtist.artist_id == db.artist.id)).select(db.artist.name).column()

    user_boxes = db(auth.user_id == db.comicbox.user_id).select(db.comicbox.name).column()

    form = SQLFORM.factory(
        Field('title', type='string', default=comicbook.title, required=True, requires=IS_NOT_EMPTY()),
        Field('box_name', type='string', required=True, default=comic_details[0].comicbox.name,
              requires=IS_IN_SET(user_boxes, zero=None)),
        Field('cover', type='upload', label='Cover max 400h * 300w px', uploadfolder=os.path.join(request.folder,'uploads'), requires=IS_EMPTY_OR(IS_IMAGE(maxsize=(300,400)))),
        Field('remove_existing_cover', type='boolean', label='Remove existing cover (automatic if cover uploaded above)', default=False),

        Field('artists', type='list:string', default=comics_artists, requires=IS_NOT_EMPTY()),
        Field('writers', type='list:string', default=comics_writers, requires=IS_NOT_EMPTY()),
        Field('publisher', type='string', default=comic_details[0].publisher.name),
        Field('update_all', type='boolean', default=False,
              label='Update the publisher of all of your comics with the same publisher.'),
        Field('issue_number', type='string', default=comicbook.issue_number),
        Field('description', type='text', default=comicbook.description), table_name='comicbook')

    if form.process().accepted:
        submit_comicedit_form(form, db, request, auth)
        session.flash = 'Sucessfully edited comic!'
        redirect(URL('comics', 'mycomics'))

    return {'form': form}


def comicdelete():
    db(db.comicbook.id == request.vars.comicbookid).delete()
    session.flash = "Deleted comic!"
    redirect(URL('comics', 'mycomics'))


def submit_comiccreate_form(form, db, request, auth):
    fields = helper.cleanupArtistsAndWritersFields(form.vars)
    # Publisher
    # If publisher already exists, get reference
    p = db((db.publisher.name == fields.publisher) & (db.publisher.user_id == auth.user_id)).select(
        db.publisher.id).column()
    if len(p) == 1:
        publisher_id = p[0]
    else:
        publisher_id = db.publisher.insert(user_id=auth.user_id, name=fields.publisher)

    # Insert comic
    boxid = db((db.comicbox.name == fields.box_name) & (db.comicbox.user_id==auth.user_id)).select(db.comicbox.id).column()[0]

    if ((fields.cover is "") | (fields.cover is None)) & (request.vars.comicbookid is not None) & (not fields.remove_existing_cover):
        rows = db(db.comicbook.id == request.vars.comicbookid).select(db.comicbook.cover)
        if len(rows)>0:
            fields.cover = rows[0].cover
    comicbook_id = db.comicbook.insert(box_id=boxid, title=fields.title, cover=fields.cover,
                                       issue_number=fields.issue_number, publisher=publisher_id)

    # Remove any empty strings in artists
    fields.artists = filter(None, fields.artists)
    fields.writers = filter(None, fields.writers)

    artist_id = []
    for art in fields.artists:
        a = db((db.artist.name == art) & (db.artist.user_id == auth.user_id)).select(db.artist.id).column()
        if len(a) == 1:
            artist_id.extend(a)
        else:
            artist_id.append(db.artist.insert(name=art, user_id=auth.user_id))

    for a_id in artist_id:
        db.comicArtist.insert(comicbook_id=comicbook_id, artist_id=a_id)

    writer_id = []
    for writer in fields.writers:
        a = db((db.writer.name == writer) & (db.writer.user_id == auth.user_id)).select(db.writer.id).column()
        if len(a) == 1:
            writer_id.extend(a)
        else:
            writer_id.append(db.writer.insert(name=writer, user_id=auth.user_id))
    for a_id in writer_id:
        db.comicWriter.insert(comicbook_id=comicbook_id, writer_id=a_id)


def submit_comicedit_form(form, db, request, auth):
    fields = helper.cleanupArtistsAndWritersFields(form.vars)

    # Updating comicbox
    boxid = db((db.comicbox.name == fields.box_name) & (db.comicbox.user_id==auth.user_id)).select(db.comicbox.id).column()[0]

    # Retrieve existing publisher_id
    publisher_id = db(db.comicbook.id == request.vars.comicbookid).select(db.comicbook.publisher).column()[0]

    if fields.update_all:
        # Update publisher field
        db(db.publisher.id == publisher_id).update(name=request.vars.publisher)
    else:
        # Find existing publisher with name and user_id in database
        existing_publisher = db(
            (db.publisher.name == request.vars.publisher) & (db.publisher.user_id == auth.user_id)).select()
        if len(existing_publisher) > 0:
            publisher_id = existing_publisher[0].id
        else:
            # If no publisher with name/user_id, create a new one
            publisher_id = db.publisher.insert(user_id=auth.user, name=request.vars.publisher)

    if ((fields.cover is "") | (fields.cover is None)) & (not fields.remove_existing_cover):
        previous_cover = db(db.comicbook.id == request.vars.comicbookid).select(db.comicbook.cover)[0].cover
        fields.cover = previous_cover

    # Update comicbook row
    db(db.comicbook.id == request.vars.comicbookid).update(title=fields.title,
                                                           box_id=boxid,
                                                           issue_number=fields.issue_number,
                                                           description=fields.description,
                                                           cover=fields.cover,
                                                           publisher=publisher_id)

    # Retrieve list of all current comicbook writer's names
    writer_names = db((db.comicWriter.writer_id == db.writer.id) & (
        db.comicWriter.comicbook_id == request.vars.comicbookid)).select(db.writer.name, groupby=db.writer.name).column()
    writer_names_to_add = list(set(fields.writers).difference(writer_names))

    # Remove all writerComic entries for this comic
    db(db.comicWriter.comicbook_id == request.vars.comicbookid).delete()

    # Add writers
    for writer in writer_names_to_add:
        # Avoid inserting duplicates
        if len(db((db.writer.user_id == auth.user_id) & (db.writer.name == writer)).select(groupby=db.writer.id)) == 0:
            db.writer.insert(user_id=auth.user_id, name=writer)

    if type(fields.writers) is str:
        fields.writers = [fields.writers]

    comic_writer_ids = db((db.writer.name.belongs(fields.writers)) & (db.writer.user_id == auth.user_id)).select(db.writer.id, groupby=db.writer.id).column()

    # Insert [comicbook_id, writer_id] pairs into comicWriter
    for writer_id in comic_writer_ids:
        if len(db((db.comicWriter.writer_id==writer_id) & (db.comicWriter.comicbook_id==request.vars.comicbookid)).select())==0:
            db.comicWriter.insert(comicbook_id=request.vars.comicbookid, writer_id=writer_id)


    # Retrieve list of all current comicbook artists's names
    artist_names = db((db.comicArtist.artist_id == db.artist.id) & (
        db.comicArtist.comicbook_id == request.vars.comicbookid)).select(db.artist.name, groupby=db.artist.name).column()
    artist_names_to_add = list(set(fields.artists).difference(artist_names))

    # Remove all artistComic entries for this comic
    db(db.comicArtist.comicbook_id == request.vars.comicbookid).delete()
    # Add artists
    for artist in artist_names_to_add:
        # Avoid inserting duplicates
        if len(db((db.artist.user_id == auth.user_id) & (db.artist.name == artist)).select(groupby=db.artist.id)) == 0:
            db.artist.insert(user_id=auth.user_id, name=artist)

    if type(fields.artists) is str:
        fields.artists = [fields.artists]
    comic_artist_ids = db(db.artist.name.belongs(fields.artists) &  (db.artist.user_id == auth.user_id)).select(db.artist.id, groupby=db.artist.id).column()

    # Insert [comicbook_id, artist_id] pairs into comicArtist
    for artist_id in comic_artist_ids:
        if len(db((db.comicArtist.artist_id==artist_id) & (db.comicArtist.comicbook_id==request.vars.comicbookid)).select())==0:

            db.comicArtist.insert(comicbook_id=request.vars.comicbookid, artist_id=artist_id)

    helper.cleanup_tables(db)