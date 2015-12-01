import os, shutil


# Remove duplicates and None from field to avoid commiting errors to the database
def cleanupArtistsAndWritersFields(fields):
    if not isinstance(fields.artists, list):
        fields.artists = [fields.artists]
    if not isinstance(fields.writers, list):
        fields.writers = [fields.writers]
    fields.artists = list(set(fields.artists))
    fields.writers = list(set(fields.writers))

    # Remove any empty strings in artists
    fields.artists = filter(None, fields.artists)
    fields.writers = filter(None, fields.writers)
    return fields

# Delete redundant data from database
def cleanup_tables(db):
    cleanup_artists(db)
    cleanup_publishers(db)
    cleanup_artists(db)


# Delete all publishers with no published comics
def cleanup_publishers(db):
    all_publishers_w_comics = db().select(db.comicbook.publisher).column()
    all_publishers_in_db = db().select(db.publisher.id).column()
    publishers_w_no_comics = list(set(all_publishers_in_db).difference(all_publishers_w_comics))
    db(db.publisher.id.belongs(publishers_w_no_comics)).delete()


# Delete all writers with no associated comics in db
def cleanup_writers(db):
    all_writers_w_comics = db().select(db.comicWriter.writer_id).column()
    all_writers_in_db = db().select(db.writer.id).column()
    writers_w_no_comics = list(set(all_writers_in_db).difference(all_writers_w_comics))
    db(db.writer.id.belongs(writers_w_no_comics)).delete()


# Delete all artists with no associated comics in db
def cleanup_artists(db):
    all_artists_w_comics = db().select(db.comicArtist.artist_id).column()
    all_artists_in_db = db().select(db.artist.id).column()
    artists_w_no_comics = list(set(all_artists_in_db).difference(all_artists_w_comics))
    db(db.artist.id.belongs(artists_w_no_comics)).delete()


# List intersection
def intersect(lists):
    s = set(lists[0])
    for l in lists:
        s &= set(l)
    return list(s)


# check if string is not None and not empty
def notempty(string):
    return (string != '') & (string is not None)


# concatenate lists
def concatlist(list):
    if list[0] is None:
        return ""
    else:
        return ", ".join(list)


# Re-allocate hanging comics to unfiled box
def move_comics_to_unfiled(db, user_id):
    unfiledBoxId = db((db.comicbox.name == "Unfiled") & (db.comicbox.user_id == user_id)).select(db.comicbox.id).column()[0]
    db(db.comicbook.box_id==None).update(box_id=unfiledBoxId)


# Re-package rows object for syntactic sugar
def re_assemble_box_with_count(box):
    re_assembled_box = box.comicbox
    re_assembled_box.count = box._extra['COUNT(comicbox.id)']
    return re_assembled_box

