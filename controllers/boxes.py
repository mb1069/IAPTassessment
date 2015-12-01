# Exam Candidate Number Y0076159

import helper

# View for individual boxes
def boxview():
    # Handle with non-existent Ids
    if len(db(db.comicbox.id == request.vars.boxid).select(db.comicbox.id)) == 0:
        session.flash = 'Box ID does not exist!'
        redirect(URL('default', 'index'))
    # Handle with private boxes
    box = db(db.comicbox.id == request.vars.boxid).select()[0]
    if box.private & (box.user_id != auth.user_id):
        session.flash = 'Box is private!'
        redirect(URL('default', 'index'))

    # Paging system
    comics_per_page = 10
    if request.vars.page is not None:
        page = int(request.vars.page)
    else:
        page = 0
    if request.vars.numitems is not None:
        numitems = int(request.vars.numitems)
    else:
        numitems = db(db.comicbook.box_id == request.vars.boxid).count()

    # Retrieve comics for box
    box_comics = db((db.comicbox.id == request.vars.boxid) & (db.comicbook.box_id == request.vars.boxid)).select(
        db.comicbook.id, db.comicbox.id, db.comicbox.user_id,
        db.comicbox.name, db.comicbook.title,
        db.comicbook.cover, db.comicbook.issue_number,
        db.comicbook.publisher, db.comicbook.description, limitby=(page * comics_per_page, (page + 1) * comics_per_page))
    record = db.comicbox(request.vars.boxid)

    # Do not allow default box to be deleted
    form = SQLFORM(db.comicbox, record, deletable=box.name!="Unfiled", submit_button="Update", delete_label="Check to delete")
    # Pre-load data
    form.vars.name = db(db.comicbox.id == request.vars.boxid).select(db.comicbox.name).column()[0]

    if form.process().accepted:
        if form.deleted:
            # Avoid orphaned comics
            helper.move_comics_to_unfiled(db, auth.user_id)
            session.flash = 'Box deleted!'
            redirect(URL('boxes', 'myboxes'))
        else:
            session.flash = 'form accepted'

    user_comics_id = []
    for row in box_comics:
        user_comics_id.append(row.comicbook.id)
    # Retrieve artists associated with comics
    artist_comics = db(
        (db.artist.id == db.comicArtist.artist_id) & (db.comicArtist.comicbook_id.belongs(user_comics_id))).select(
        db.comicArtist.comicbook_id, db.artist.name)
    # Retrieve writers associated with comics
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
            "display_next": numitems>(page+1)*comics_per_page}

# View to create new box and redirect to box on success
def boxcreate():
    form = SQLFORM(db.comicbox)
    form.vars.user_id = auth.user_id
    if form.process().accepted:
        session.flash = 'Created box!'
        redirect(URL('boxes', 'boxview', vars={'boxid': form.vars.id}))
    return {'form': form}

# View to display all of user's boxes
def myboxes():
    # Paging
    items_per_page = 10
    if len(request.args):
        page = int(request.args[0])
    else:
        page = 0
    if len(request.args) == 2:
        numitems = int(request.args[1])
    else:
        numitems = db(auth.user_id == db.comicbox.user_id).count()

    # Retrieve user boxes
    user_boxes = db(auth.user_id == db.comicbox.user_id).select(
        db.comicbox.id,
        db.comicbox.name,
        db.comicbox.created_on,
        groupby=db.comicbox.name, limitby=(page * items_per_page, (page + 1) * items_per_page))

    boxes = []
    # Retrieve data associated with boxes and compact into tuples
    for box in user_boxes:
        comics = db(db.comicbook.box_id == box.id).select(db.comicbook.title,
                                                          db.comicbook.cover, db.comicbook.description,
                                                          db.comicbook.issue_number, db.comicbook.publisher)
        box.count = len(comics)
        boxes.append((box, comics))
    return {'user_boxes': boxes, 'page': page,
            'display_next': numitems>(page+1)*items_per_page}
