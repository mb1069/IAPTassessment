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
import os
import time
import helper


def index():
    largest_boxes = get_largest_boxes(5)
    recent_boxes = get_recent_boxes(5)
    return {'largest_boxes': largest_boxes, 'recent_boxes': recent_boxes}


def search():
    form = SQLFORM.factory(
        Field('keyword', type='string'),
        Field('title', type='string'),
        Field('writer', type='string'),
        Field('artist', type='string'),
        Field('publisher', type='string'),
        Field('keyword', type='string'))
    search_results = []
    if form.process().accepted:
        fields = form.vars
        field_results = []

        if helper.notempty(fields.keyword):
            # Search all fields and intersect
            print 'keyword'
            keyword_results = db(db.comicbook.title.like('%' + fields.keyword + '%')).select(db.comicbook.id).column(
                    db.comicbook.id)

            keyword_results.extend(db((db.publisher.name.like('%' + fields.keyword + '%'))
                                 & (db.comicbook.publisher == db.publisher.id)) \
                                .select(db.comicbook.id).column(db.comicbook.id))

            keyword_results.extend(db(db.writer.name.like('%' + fields.keyword + '%') &
                                      (db.comicWriter.writer_id == db.writer.id) &
                                      (db.comicbook.id == db.comicWriter.comicbook_id))
                .select(db.comicbook.id).column(db.comicbook.id))

            keyword_results.extend(db(db.artist.name.like('%' + fields.keyword + '%') &
                                      (db.comicArtist.artist_id == db.artist.id) &
                                      (db.comicbook.id == db.comicArtist.comicbook_id)).select(db.comicbook.id).column(
                db.comicbook.id))
            field_results.append(keyword_results)

        if helper.notempty(fields.title):
            print 'title'
            field_results.append(
                db(db.comicbook.title.like('%' + fields.title + '%')).select(db.comicbook.id).column(
                    db.comicbook.id))

        if helper.notempty(fields.publisher):
            print 'publisher'
            field_results.append(
                db((db.publisher.name.like('%' + fields.publisher + '%')) & (
                    db.comicbook.publisher == db.publisher.id)).select(db.comicbook.id).column(
                    db.comicbook.id))

        if helper.notempty(fields.writer):
            print 'writer'
            field_results.append(db(db.writer.name.like('%' + fields.writer + '%') &
                                    (db.comicWriter.writer_id == db.writer.id) &
                                    (db.comicbook.id == db.comicWriter.comicbook_id)).select(db.comicbook.id).column(
                db.comicbook.id))

        if helper.notempty(fields.artist):
            print 'artist'
            field_results.append(db(db.artist.name.like('%' + fields.artist + '%') &
                                    (db.comicArtist.artist_id == db.artist.id) &
                                    (db.comicbook.id == db.comicArtist.comicbook_id)).select(db.comicbook.id).column(
                db.comicbook.id))

        if len(field_results) > 0:
            intersected_results = helper.intersect(field_results)

            left_joins = [db.comicWriter.on(db.comicWriter.comicbook_id == db.comicbook.id),
                          db.writer.on(db.comicWriter.writer_id == db.writer.id),
                          db.comicArtist.on(db.comicArtist.comicbook_id == db.comicbook.id),
                          db.artist.on(db.comicArtist.artist_id == db.artist.id)]

            search_results = db(db.comicbook.id.belongs(intersected_results)).select(db.comicbook.title,
                                                                                     db.comicbook.id,
                                                                                     db.comicbook.issue_number,
                                                                                     db.comicbook.box_id,
                                                                                     db.artist.name, db.writer.name,
                                                                                     left=left_joins)

    elif form.errors:
        return form.errors
    return {'search_results': search_results, 'form2': form}


def get_largest_boxes(num_boxes):
    count = db.comicbox.id.count()
    largest_boxes = db(db.comicbox.id == db.comicbook.box_id).select(db.comicbox.id, db.comicbox.name,
                                                                     db.comicbox.created_on, count, orderby=~count,
                                                                     groupby=db.comicbox.id, limitby=(0, num_boxes))

    boxes = []
    for box in largest_boxes:
        comics = db(db.comicbook.box_id == box.comicbox.id).select(db.comicbook.title, db.comicbook.cover,
                                                                   db.comicbook.description, db.comicbook.issue_number,
                                                                   db.comicbook.publisher)
        boxes.append((re_assemble_box_with_count(box), comics))

    return boxes


def get_recent_boxes(num_boxes):
    count = db.comicbox.id.count()
    recent_boxes = db(db.comicbox.id == db.comicbook.box_id).select(db.comicbox.id, db.comicbox.name,
                                                                    db.comicbox.created_on, count,
                                                                    orderby=~db.comicbox.created_on,
                                                                    groupby=db.comicbox.id, limitby=(0, num_boxes))
    boxes = []
    for box in recent_boxes:
        comics = db(db.comicbook.box_id == box.comicbox.id).select(db.comicbook.title,
                                                                   db.comicbook.cover, db.comicbook.description,
                                                                   db.comicbook.issue_number, db.comicbook.publisher)
        boxes.append((re_assemble_box_with_count(box), comics))

    return boxes


def re_assemble_box_with_count(box):
    re_assembled_box = box.comicbox
    re_assembled_box.count = box._extra['COUNT(comicbox.id)']
    return re_assembled_box


def error():
    return {'errormsg': request.vars.errormsg}


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


def fast_download():
    # very basic security (only allow fast_download on db.comicbook.cover):
    if not request.args(0).startswith("db.comicbook.cover"):
        return download()
    # remove/add headers that prevent/favors client-side caching
    # 7days
    response.headers['Cache-Control'] = "max-age=604800"
    del response.headers['Pragma']
    del response.headers['Expires']
    filename = os.path.join(request.folder, 'uploads', request.args(0))
    # send last modified date/time so client browser can enable client-side caching
    print filename
    response.headers['Last-Modified'] = time.strftime("%a, %d %b %Y %H:%M:%S +0000",
                                                      time.localtime(os.path.getmtime(filename)))

    return response.stream(open(filename, 'rb'))


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
