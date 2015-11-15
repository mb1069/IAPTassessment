def submit_newcomic_form(form, db, request, auth):
    print 'a'


def submit_comicedit_form(form, db, request, auth):
    fields = form.vars

    # Updating comicbox
    boxid = db(db.comicbox.name == fields.box_name).select(db.comicbox.id).column()[0]

    # Retrieve existing publisher_id
    publisher_id = db(db.comicbook.id == request.vars.comicbookid).select(db.comicbook.publisher).column()[0]

    if fields.update_all:
        # Update publisher field
        db(db.publisher.id == publisher_id).update(name=request.vars.publisher)
    else:
        # Find existing publisher with name and user_id in database
        existing_publisher = db(
            (db.publisher.name == request.vars.publisher) & (db.publisher.user_id == auth.user_id)).select()
        if len(existing_publisher) > 0:
            publisher_id = existing_publisher[0].id
        else:
            # If no publisher with name/user_id, create a new one
            publisher_id = db.publisher.insert(user_id=auth.user, name=request.vars.publisher)

    # Update comicbook row
    db(db.comicbook.id == request.vars.comicbookid).update(title=fields.title,
                                                           box_id=boxid,
                                                           issue_number=fields.issue_number,
                                                           description=fields.description,
                                                           publisher=publisher_id)

    # Retrieve list of all current comicbook writer's names
    writer_names = db((db.comicWriter.writer_id == db.writer.id) & (
        db.comicWriter.comicbook_id == request.vars.comicbookid)).select(db.writer.name).column()
    writer_names_to_add = list(set(fields.writers).difference(writer_names))

    # Remove all writerComic entries for this comic
    db(db.comicWriter.comicbook_id == request.vars.comicbookid).delete()

    # Add writers
    for writer in writer_names_to_add:
        # Avoid inserting duplicates
        if len(db((db.writer.user_id == auth.user_id) & (db.writer.name == writer)).select()) == 0:
            db.writer.insert(user_id=auth.user_id, name=writer)

    if type(fields.writers) is str:
        fields.writers = [fields.writers]

    comic_writer_ids = db(db.writer.name.belongs(fields.writers)).select(db.writer.id).column()

    # Insert [comicbook_id, writer_id] pairs into comicWriter
    for writer_id in comic_writer_ids:
        db.comicWriter.insert(comicbook_id=request.vars.comicbookid, writer_id=writer_id)


    # Retrieve list of all current comicbook artists's names
    artist_names = db((db.comicArtist.artist_id == db.artist.id) & (
        db.comicArtist.comicbook_id == request.vars.comicbookid)).select(db.artist.name).column()
    artist_names_to_add = list(set(fields.artists).difference(artist_names))

    # Remove all artistComic entries for this comic
    print db(db.comicArtist.comicbook_id == request.vars.comicbookid).select()
    db(db.comicArtist.comicbook_id == request.vars.comicbookid).delete()
    print 'after delete ', db(db.comicArtist.comicbook_id == request.vars.comicbookid).select(
        db.comicArtist.artist_id).column()

    # Add artists
    for artist in artist_names_to_add:
        # Avoid inserting duplicates
        if len(db((db.artist.user_id == auth.user_id) & (db.artist.name == artist)).select()) == 0:
            db.artist.insert(user_id=auth.user_id, name=artist)

    if type(fields.artists) is str:
        fields.artists = [fields.artists]
    comic_artist_ids = db(db.artist.name.belongs(fields.artists)).select(db.artist.id).column()

    # Insert [comicbook_id, artist_id] pairs into comicArtist
    for artist_id in comic_artist_ids:
        db.comicArtist.insert(comicbook_id=request.vars.comicbookid, artist_id=artist_id)

    cleanup_tables(db)


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
