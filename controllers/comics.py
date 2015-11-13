__author__ = 'miguel'


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
    # verify owner owns the comicbook
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
    comic_book_id = comic_details[0].comicbook.id
    comics_writers = db((db.comicWriter.comicbook_id == comic_book_id) & (db.comicWriter.writer_id == db.writer.id)) \
        .select(db.writer.name).column()
    comics_artists = db((db.comicArtist.comicbook_id == comic_book_id) & (db.comicArtist.artist_id == db.artist.id)) \
        .select(db.artist.name).column()
    comicbook = comic_details[0].comicbook
    print 'comicbook'
    print comicbook
    form = SQLFORM.factory(
        Field('title', type='string', default=comicbook.title),
        Field('box_name', type='string', default=comic_details[0].comicbox.name),
        # add requires is in box and is owned by user
        Field('cover', type='upload', default=comicbook.cover),
        Field('artists', type='list:string', default=comics_artists),
        Field('writers', type='list:string', default=comics_writers),
        Field('publisher', type='string', default=comic_details[0].publisher.name),
        Field('issue_number', type='string', default=comicbook.issue_number),
        Field('description', default=comicbook.description))
    print 'processing'
    if form.process().accepted:
        print 'accepted'
        return 'accepted'
    elif form.errors:
        print 'errors'
        return 'errors'

    if len(comic_details) == 0:
        redirect(URL('default', 'error', vars={
            'errormsg': 'An error has occured: comicbook was not found in database.'}))
    else:

        user_boxes = db(auth.user_id == db.comicbox.user_id).select(db.comicbox.name)
        # existing_publishers = db().select(db.publisher.name)
        # existing_artists = db().select(db.artist.name).column()
        # existing_writers = db().select(db.writer.name).column()

        return {'comic': comic_details[0], 'form': form, 'comicbook_details': comic_details, 'user_boxes': user_boxes
                # ,'existing_publishers': existing_publishers, 'existing_artists': existing_artists,'existing_writers': existing_writers,
                }
