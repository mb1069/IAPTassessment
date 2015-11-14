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
    # Verify comicbookid exists
    if (request.vars.comicbookid is None) | (len(request.vars.comicbookid) == 0):
        redirect(URL('default', 'error', vars={
            'errormsg': 'Error: no coming book selected for editing'}))

    user_boxes = db(auth.user_id == db.comicbox.user_id).select(db.comicbox.name).column()

    # Verify user owns comicbook
    # TODO finish writing and test with multiple users
    if auth.user_id != db(
                    (request.vars.comicbookid == db.comicbook.id) & (db.comicbook.box_id == db.comicbox.id)).select(
        db.comicbox.user_id).column()[0]:
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
        Field('artists', type='list:string', default=comics_artists),
        Field('writers', type='list:string', default=comics_writers),
        Field('publisher', type='string', default=comic_details[0].publisher.name),
        Field('issue_number', type='string', default=comicbook.issue_number),
        Field('description', default=comicbook.description))
    if form.process().accepted:
        fields = form.vars

        # Updating comicbox
        boxid = db(db.comicbox.name == fields.box_name).select(db.comicbox.id).column()[0]

        # Update publisher
        publisher = db(db.comicbook.id == request.vars.comicbookid).select(db.comicbook.publisher).column()[0]
        # If only this comicbook references publisher, update publisher
        if db(db.comicbook.publisher == publisher).count() == 1:
            db(db.publisher.id == publisher).update(name=request.vars.publisher)
        # Else create new publisher
        else:
            publisher = db.publisher.insert(user_id=auth.user, name=request.vars.publisher)

        # TODO delete publishers with no comics


        # Update comicbook row
        db(db.comicbook.id == request.vars.comicbookid).update(title=fields.title,
                                                               box_id=boxid,
                                                               issue_number=fields.issue_number,
                                                               description=fields.description,
                                                               publisher=publisher)
        # TODO finish implementing/verify this actually works
        # Retrieve list of all current comicbook writer's names
        writer_names = db((db.comicWriter.writer_id == db.writer.id) & (db.comicWriter.comicbook_id == request.vars.comicbookid)).select(db.writer.name).column()
        writer_names_to_add = list(set(fields.writers).difference(writer_names))

        # Remove all writerComic entries for this comic
        db(db.comicWriter.comicbook_id == request.vars.comicbookid).delete()
        print 'after delete ', db(db.comicWriter.comicbook_id==request.vars.comicbookid).select(db.comicWriter.writer_id).column()

        # Add writers
        for writer in writer_names_to_add:
            db.writer.insert(user_id=auth.user_id, name=writer)

        comic_writer_ids = db(db.writer.name.belongs(writer_names)).select(db.writer.id).column()
        for writer_id in comic_writer_ids:
            db.comicWriter.insert(comicbook_id=request.vars.comicbookid, writer_id=writer_id)

        return 'accepted'
    elif form.errors:
        return 'error'

        # existing_publishers = db().select(db.publisher.name)
        # existing_artists = db().select(db.artist.name).column()
        # existing_writers = db().select(db.writer.name).column()

    return {'comic': comic_details[0], 'form': form, 'comicbook_details': comic_details, 'user_boxes': user_boxes}
