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
    artist_comics = db((db.artist.id == db.comicArtist.artist) & (db.comicArtist.comicbook.belongs(user_comics_id))).select(db.comicArtist.comicbook, db.artist.name)
    writer_comics = db((db.writer.id == db.comicWriter.writer) & (db.comicWriter.comicbook.belongs(user_comics_id))).select(db.comicWriter.comicbook, db.writer.name)

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
    return {}