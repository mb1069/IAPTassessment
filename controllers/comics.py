__author__ = 'miguel'


def mycomics():
    user_comics = db((auth.user_id == db.comicbox.user_id) &
                     (db.comicbox.id == db.comicbook.box_id)).select(db.comicbook.id, db.comicbox.id,
                                                                     db.comicbox.box_name, db.comicbook.title,
                                                                     db.comicbook.cover, db.comicbook.issue_number,
                                                                     db.comicbook.publisher, db.comicbook.description)

    # search_results = db((db.comicbox.user_id == auth.user_id) & (db.comicbox.id == db.comicbook.box_id)).select(
    #             left=[db.comicWriter.on(db.comicWriter.comicbook == db.comicbook.id),
    #                   db.writer.on(db.comicWriter.writer == db.writer.id),
    #                   db.comicArtist.on(db.comicArtist.comicbook == db.comicbook.id),
    #                   db.artist.on(db.comicArtist.artist == db.artist.id)])
    # return {'user_comics': user_comics, 'search_results': search_results}
    return {'user_comics': user_comics}


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


def download():
    return response.download(request, db)
