import helper


def boxview():
    # Deal with non-existent Ids
    if len(db(db.comicbox.id == request.vars.boxid).select(db.comicbox.id)) == 0:
        session.flash = 'Box ID does not exist!'
        redirect(URL('default', 'index'))
    # Deal with private boxes
    box = db(db.comicbox.id == request.vars.boxid).select()[0]

    if box.private & (box.user_id != auth.user_id):
        session.flash = 'Box is private!'
        redirect(URL('default', 'index'))

    items_per_page = 5

    if request.vars.page is not None:
        page = int(request.vars.page)
    else:
        page = 0
    if len(request.args) == 2:
        numitems = int(request.vars.numitems)
    else:
        numitems = db(db.comicbook.box_id == request.vars.boxid).count()

    box_comics = db((db.comicbox.id == request.vars.boxid) & (db.comicbook.box_id == request.vars.boxid)).select(
        db.comicbook.id, db.comicbox.id,
        db.comicbox.name, db.comicbook.title,
        db.comicbook.cover, db.comicbook.issue_number,
        db.comicbook.publisher, db.comicbook.description, limitby=(page * items_per_page, (page + 1) * items_per_page))
    record = db.comicbox(request.vars.boxid)
    form = SQLFORM(db.comicbox, record, deletable=True, submit_button="Update", delete_label="Check to delete")
    form.vars.name = db(db.comicbox.id == request.vars.boxid).select(db.comicbox.id).column()[0]

    if form.process().accepted:

        if form.deleted:
            helper.move_comics_to_unfiled(db, auth.user_id)
            session.flash = 'Box deleted!'
            redirect(URL('boxes', 'myboxes'))
        else:
            session.flash = 'form accepted'

    user_comics_id = []
    for row in box_comics:
        user_comics_id.append(row.comicbook.id)
    artist_comics = db(
        (db.artist.id == db.comicArtist.artist_id) & (db.comicArtist.comicbook_id.belongs(user_comics_id))).select(
        db.comicArtist.comicbook_id, db.artist.name)
    writer_comics = db(
        (db.writer.id == db.comicWriter.writer_id) & (db.comicWriter.comicbook_id.belongs(user_comics_id))).select(
        db.comicWriter.comicbook_id, db.writer.name)

    return {'boxdetails': db(db.comicbox.id == request.vars.boxid).select()[0],
            'box_comics': box_comics,
            'artist_comics': artist_comics,
            'writer_comics': writer_comics,
            'form': form,
            "page": page,
            "numitems": numitems,
            "display_next": numitems>(page+1)*items_per_page}


def boxcreate():
    form = SQLFORM(db.comicbox)
    form.vars.user_id = auth.user_id
    if form.process().accepted:
        session.flash = 'Created box!'
        redirect(URL('boxes', 'myboxes'))
    return {'form': form}


def myboxes():
    items_per_page = 10

    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    if len(request.args) == 2:
        numitems = int(request.args[1])
    else:
        numitems = db(auth.user_id == db.comicbox.user_id).count()

    user_boxes = db(auth.user_id == db.comicbox.user_id).select(
        db.comicbox.id,
        db.comicbox.name,
        db.comicbox.created_on,
        groupby=db.comicbox.name, limitby=(page * items_per_page, (page + 1) * items_per_page))




    boxes = []
    for box in user_boxes:
        comics = db(db.comicbook.box_id == box.id).select(db.comicbook.title,
                                                          db.comicbook.cover, db.comicbook.description,
                                                          db.comicbook.issue_number, db.comicbook.publisher)
        box.count = len(comics)
        boxes.append((box, comics))
    return {'user_boxes': boxes, 'page': page,
            'display_next': numitems>(page+1)*items_per_page}