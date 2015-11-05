__author__ = 'miguel'


def myboxes():

    user_boxes = db(auth.user_id == db.comicbox.user_id).select('comicbox.id', 'comicbox.box_name')

    user_comics = db((auth.user_id == db.comicbox.user_id) &
                   (db.comicbox.id == db.comicbook.box_id)).select()

    return {'user_comics': user_comics, 'user_boxes': user_boxes}


def download():
    return response.download(request, db)
