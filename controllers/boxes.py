import helper


def boxview():
    boxid = request.vars.boxid

    return {"boxid": boxid,
            "boxdetails": db(db.comicbox.id == boxid).select()}


def myboxes():
    user_boxes = db(auth.user_id == db.comicbox.user_id).select(
        db.comicbox.id,
        db.comicbox.name,
        db.comicbox.created_on,
        groupby=db.comicbox.name)

    boxes = []
    for box in user_boxes:
        comics = db(db.comicbook.box_id == box.id).select(db.comicbook.title,
                                                          db.comicbook.cover, db.comicbook.description,
                                                          db.comicbook.issue_number, db.comicbook.publisher)
        box.count = len(comics)
        boxes.append((box, comics))
    return {'user_boxes': boxes}
