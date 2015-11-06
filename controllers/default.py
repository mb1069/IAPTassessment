# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

########################################################################
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
########################################################################


# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

########################################################################
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
########################################################################


def index():

    largest_boxes = get_biggest_boxes(5)
    recent_boxes = get_recent_boxes(5)

    return {'largest_boxes': largest_boxes, 'recent_boxes': recent_boxes}


def get_biggest_boxes(num_boxes):
    count = db.comicbox.id.count()
    boxes = db(db.comicbox.id == db.comicbook.box_id).select(db.comicbox.id,
                                                             count,
                                                             orderby=~count,
                                                             groupby=db.comicbox.box_name,
                                                             limitby=(0, num_boxes))

    boxed_comics = []
    for row in boxes:
        boxed_comics.append(db((db.comicbook.box_id == row.comicbox.id) & (row.comicbox.id == db.comicbox.id)).select(
            db.comicbook.title,
            db.comicbook.cover,
            db.comicbox.box_name, db.comicbox.created_on))
    return boxed_comics


def get_recent_boxes(num_boxes):
    boxes = db().select(db.comicbox.id,
                        db.comicbox.box_name,
                        db.comicbox.created_on,
                        orderby=~db.comicbox.created_on,
                        limitby=(0, num_boxes))
    boxed_comics = []
    for row in boxes:
        boxed_comics.append(
            db((db.comicbook.box_id == row.id) & (row.id == db.comicbox.id)).select(db.comicbook.title,
                                                                                    db.comicbook.cover,
                                                                                    db.comicbox.box_name, db.comicbox.created_on))
    return boxed_comics


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
