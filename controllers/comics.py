__author__ = 'miguel'

import helper


def mycomics():
    user_comics = db((auth.user_id == db.comicbox.user_id) &
                     (db.comicbox.id == db.comicbook.box_id)).select(db.comicbook.id, db.comicbox.id,
                                                                     db.comicbox.name, db.comicbook.title,
                                                                     db.comicbook.cover, db.comicbook.issue_number,
                                                                     db.comicbook.publisher, db.comicbook.description)
    user_comics_id = []
    for row in user_comics:
        user_comics_id.append(row.comicbook.id)

    artist_comics = db(
        (db.artist.id == db.comicArtist.artist_id) & (db.comicArtist.comicbook_id.belongs(user_comics_id))).select(
        db.comicArtist.comicbook_id, db.artist.name)
    writer_comics = db(
        (db.writer.id == db.comicWriter.writer_id) & (db.comicWriter.comicbook_id.belongs(user_comics_id))).select(
        db.comicWriter.comicbook_id, db.writer.name)

    return {'user_comics': user_comics, 'artist_comics': artist_comics, 'writer_comics': writer_comics}
    # return {'user_comics': user_comics}


def myboxes():
    user_boxes = db(auth.user_id == db.comicbox.user_id).select(
        db.comicbox.id,
        db.comicbox.name,
        db.comicbox.created_on,
        groupby=db.comicbox.name)

    boxes = []
    for box in user_boxes:
        comics = db(db.comicbook.box_id == box.id).select(db.comicbook.title,
                                                          db.comicbook.cover, db.comicbook.description,
                                                          db.comicbook.issue_number, db.comicbook.publisher)
        box.count = len(comics)
        boxes.append((box, comics))
    return {'user_boxes': boxes}


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
    print db((db.comicbox.user_id == auth.user_id) & (db.comicbook.box_id == db.comicbox.id)).select(
            db.comicbook.id).column()
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

    comics_writers = db((db.comicWriter.comicbook_id == request.vars.comicbookid) &
                        (db.comicWriter.writer_id == db.writer.id)).select(db.writer.name).column()
    comics_artists = db((db.comicArtist.comicbook_id == request.vars.comicbookid) &
                        (db.comicArtist.artist_id == db.artist.id)).select(db.artist.name).column()
    comicbook = comic_details[0].comicbook

    user_boxes = db(auth.user_id == db.comicbox.user_id).select(db.comicbox.name).column()

    form = SQLFORM.factory(
        Field('title', type='string', default=comicbook.title, required=True, requires=IS_NOT_EMPTY()),
        Field('box_name', type='string', required=True, default=comic_details[0].comicbox.name,
              requires=IS_IN_SET(user_boxes, zero=None)),
        Field('cover', type='upload', uploadfolder='upload'),
        Field('artists', type='list:string', default=comics_artists, requires=IS_NOT_EMPTY()),
        Field('writers', type='list:string', default=comics_writers, requires=IS_NOT_EMPTY()),
        Field('publisher', type='string', default=comic_details[0].publisher.name),
        Field('update_all', type='boolean', default=False, label='Update publisher for all comics'),
        Field('issue_number', type='string', default=comicbook.issue_number),
        Field('description', default=comicbook.description))

    if form.process().accepted:
        helper.submit_comicedit_form(form, db, request, auth)
        return 'accepted'
    elif form.errors:
        return 'error'

    return {'form': form}
