__author__ = 'mb1069'

import os

# db(db.comicbox.id > 0).delete()
# db(db.comicbook.id > 0).delete()
# db.comicArtist.truncate()
# db.comicWriter.truncate()
# db(db.publisher.id > 0).delete()

crypt = CRYPT(key=auth.settings.hmac_key)
# for i in range(1, 6):
#     db.auth_user.insert(id=i, first_name='Test', last_name='User %s' % i, email='test_email_%s@sososofake.com' % i, password=crypt('password%s' % i)[0])
#     db.auth_group.insert(id=i, role='user%s' % i, description='Group uniquely assigned to user %s' % i)
#     db.auth_membership.insert(id=i, user_id=i, group_id=i)
i = 1
if db(db.auth_user.id >= 0).count() == 0:
    db.auth_user.insert(id=i, first_name='dadude941', last_name='User %s' % i, email='test_email_%s@sososofake.com' % i,
                        password=crypt('password%s' % i)[0])
if db(db.auth_user.id > 0).count() == 0:
    db.auth_user.insert(id=i, first_name='dadude941', last_name='User %s' % i, email='test_email_%s@sososofake.com' % i,
                        password=crypt('aa')[0])
    db.auth_group.insert(id=i, role='user%s' % i, description='Group uniquely assigned to user %s' % i)
    db.auth_membership.insert(id=i, user_id=i, group_id=i)

if db(db.comicbox.id > 0).count() == 0:
    db.publisher.insert(user_id=1, name='DC')
    db.publisher.insert(user_id=1, name='Marvel')

    db.comicbox.insert(user_id=1, name='Box A', private=True)
    db.comicbox.insert(user_id=1, name='Box B', private=True)
    db.comicbox.insert(user_id=1, name='Box C', private=True)
    db.comicbox.insert(user_id=1, name='Box D', private=True)
    db.comicbox.insert(user_id=1, name='Box E', private=True)
    db.comicbox.insert(user_id=1, name='Box F', private=True)

    cover_path = os.path.join(os.path.dirname(__file__), '../static/images/superman.jpg')

    db.comicbook.insert(box_id=1, title='Superman1', publisher=1, issue_number=949, cover=open(cover_path), description='In the past, yet also in the future, in a land far far away in space...')
    db.comicbook.insert(box_id=2, title='Superman2', publisher=2, cover=open(cover_path))
    db.comicbook.insert(box_id=2, title='Superman2', publisher=1, cover=open(cover_path))
    db.comicbook.insert(box_id=3, title='Superman3', publisher=2, cover=open(cover_path))
    db.comicbook.insert(box_id=3, title='Superman3', publisher=1, cover=open(cover_path))
    db.comicbook.insert(box_id=3, title='Superman3', publisher=2, cover=open(cover_path))
    db.comicbook.insert(box_id=4, title='Superman4', publisher=1, cover=open(cover_path))
    db.comicbook.insert(box_id=4, title='Superman4', publisher=2, cover=open(cover_path))
    db.comicbook.insert(box_id=4, title='Superman4', publisher=1, cover=open(cover_path))
    db.comicbook.insert(box_id=4, title='Superman4', publisher=2, cover=open(cover_path))
    db.comicbook.insert(box_id=5, title='Superman5', publisher=1, cover=open(cover_path))
    db.comicbook.insert(box_id=5, title='Superman5', publisher=2, cover=open(cover_path))
    db.comicbook.insert(box_id=5, title='Superman5', publisher=1, cover=open(cover_path))
    db.comicbook.insert(box_id=5, title='Superman5', publisher=2, cover=open(cover_path))
    db.comicbook.insert(box_id=5, title='Superman5', publisher=1, cover=open(cover_path))
    db.comicbook.insert(box_id=5, title='Superman5', publisher=2, cover=open(cover_path))

    db.artist.insert(user_id=1, name='Artsy')
    db.artist.insert(user_id=1, name='Art')
    db.comicArtist.insert(comicbook_id=1, artist_id=1)
    db.comicArtist.insert(comicbook_id=1, artist_id=2)
    db.writer.insert(user_id=1, name='Writsy')
    db.writer.insert(user_id=1, name='Writ')
    db.comicWriter.insert(comicbook_id=1, writer_id=1)
    db.comicWriter.insert(comicbook_id=1, writer_id=2)
