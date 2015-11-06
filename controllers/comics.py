__author__ = 'miguel'


def mycomics():

    user_comics = db((auth.user_id == db.comicbox.user_id) &
                   (db.comicbox.id == db.comicbook.box_id)).select(db.comicbook.id, db.comicbox.id, db.comicbox.box_name, db.comicbook.title, db.comicbook.cover, db.comicbook.issue_number, db.comicbook.publisher, db.comicbook.description)
    return {'user_comics': user_comics}


def myboxes():
    user_boxes = db(auth.user_id == db.comicbox.user_id).select('comicbox.id', 'comicbox.box_name')

    return {'user_boxes': user_boxes}


def download():
    return response.download(request, db)
