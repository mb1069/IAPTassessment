__author__ = 'miguel'


def mycomics():
    user_comics = db((auth.user_id == db.comicbox.user_id) &
                     (db.comicbox.id == db.comicbook.box_id)).select(db.comicbook.id, db.comicbox.id,
                                                                     db.comicbox.box_name, db.comicbook.title,
                                                                     db.comicbook.cover, db.comicbook.issue_number,
                                                                     db.comicbook.publisher, db.comicbook.description)
    return {'user_comics': user_comics}


def myboxes():
    user_box_data = db((auth.user_id == db.comicbox.user_id) & (db.comicbook.box_id == db.comicbox.id)).select('box_name',
                                                                                                               'box_id',
                                                                                                               'title',
                                                                                                               'cover',
                                                                                                               'created_on',
                                                                                                               'issue_number',
                                                                                                               'publisher',
                                                                                                               'description')
    user_box_names = db((auth.user_id == db.comicbox.user_id) & (db.comicbook.box_id == db.comicbox.id)).select(
        db.comicbox.id, db.comicbox.box_name, db.comicbox.created_on, groupby='box_name')
    return {'user_boxes_data': user_box_data, 'user_box_names': user_box_names}


def download():
    return response.download(request, db)
