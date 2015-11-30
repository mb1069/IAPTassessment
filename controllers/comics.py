__author__ = 'miguel'

import helper


def mycomics():
    items_per_page = 10

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
                                                                     db.comicbox.name, db.comicbook.title,
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
    defaultCover = comicdata.get('cover', '')

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
        Field('cover', type='upload', default=defaultCover, uploadfolder='uploads', requires=IS_EMPTY_OR(IS_IMAGE())),
        Field('artists', type='list:string', default=defaultArtists),
        Field('writers', type='list:string', default=defaultWriters),
        Field('publisher', type='string', default=defaultPublisher),
        Field('issue_number', type='integer', default=defaultIssue_number),
        Field('description', type='text', default=defaultDescription),
        table_name='comicbook', upload=URL('uploads'))

    if form.process().accepted:
        helper.submit_comiccreate_form(form, db, request, auth)
        ##TODO add confirmation message
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
        Field('cover', type='upload', uploadfolder='upload'),
        Field('artists', type='list:string', default=comics_artists, requires=IS_NOT_EMPTY()),
        Field('writers', type='list:string', default=comics_writers, requires=IS_NOT_EMPTY()),
        Field('publisher', type='string', default=comic_details[0].publisher.name),
        Field('update_all', type='boolean', default=False,
              label='Update the publisher of all of your comics with the same publisher.'),
        Field('issue_number', type='string', default=comicbook.issue_number),
        Field('description', type='text', default=comicbook.description), table_name='comicbook')

    if form.process().accepted:
        helper.submit_comicedit_form(form, db, request, auth)
        # TODO add confirmation of success message
        redirect(URL('comics', 'mycomics'))

    return {'form': form}


def comicdelete():
    db(db.comicbook.id == request.vars.comicbookid).delete()
    redirect(URL('comics', 'mycomics'))
