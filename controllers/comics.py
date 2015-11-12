__author__ = 'miguel'


def mycomics():
    user_comics = db((auth.user_id == db.comicbox.user_id) &
                     (db.comicbox.id == db.comicbook.box_id)).select(db.comicbook.id, db.comicbox.id,
                                                                     db.comicbox.box_name, db.comicbook.title,
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
        db.comicbox.box_name,
        db.comicbox.created_on,
        groupby=db.comicbox.box_name)

    boxes = []
    for box in user_boxes:
        comics = db(db.comicbook.box_id == box.id).select(db.comicbook.title,
                                                          db.comicbook.cover, db.comicbook.description,
                                                          db.comicbook.issue_number, db.comicbook.publisher)
        box.count = len(comics)
        boxes.append((box, comics))
    return {'user_boxes': boxes}


def comicedit():
    ##verify owner owns the comicbook
    left_joins = [db.comicWriter.on(db.comicWriter.comicbook_id == db.comicbook.id),
                  db.writer.on(db.comicWriter.writer_id == db.writer.id),
                  db.comicArtist.on(db.comicArtist.comicbook_id == db.comicbook.id),
                  db.artist.on(db.comicArtist.artist_id == db.artist.id)]

    search_results = db(db.comicbook.id == request.vars.comicbookid).select(db.comicbook.title, db.comicbook.id,
                                                                            db.comicbook.issue_number,
                                                                            db.comicbook.box_id,
                                                                            db.artist.name, db.writer.name,
                                                                            db.comicbook.cover,
                                                                            left=left_joins)

    existing_publishers = db().select(db.publisher.name)
    existing_artists = db().select(db.artist.name)
    existing_writers = db().select(db.writer.name)

    return {'existing_publishers': existing_publishers, 'existing_artists': existing_artists,
            'existing_writers': existing_writers, 'comicbook_details': search_results}
