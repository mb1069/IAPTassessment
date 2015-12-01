# coding=utf-8

import os

# db(db.comicbox.id > 0).delete()
# db(db.comicbook.id > 0).delete()
# db.comicArtist.truncate()
# db.comicWriter.truncate()
# db(db.publisher.id > 0).delete()
import random

crypt = CRYPT(key=auth.settings.hmac_key)
# for i in range(1, 6):
#     db.auth_user.insert(id=i, first_name='Test', last_name='User %s' % i, email='test_email_%s@sososofake.com' % i, password=crypt('password%s' % i)[0])
#     db.auth_group.insert(id=i, role='user%s' % i, description='Group uniquely assigned to user %s' % i)
#     db.auth_membership.insert(id=i, user_id=i, group_id=i)

i = 1
if db(db.auth_user.id >= 0).count() == 0:
    for i in range(0, 10):
        db.auth_user.insert(id=i, username='username%s' % i, first_name='username%s' % i, last_name='User %s' % i, email='test_email_%s@sososofake.com' % i,
                        password=crypt('password%s' % i)[0])

templateComics = [
    {"title": "The Uncanny X-MEN: Days of Future Past", "publisher": "Marvel Comics", "issue_number": "#141" ,"cover_path":"x-men-days-of-future-past.jpg" , "writers": ["Chris Claremont", "John Byrne"], "artists":["John Byrne", "Terry Austin"] ,"description": "Re-live the legendary first journey into the dystopian future of 2013 - where Sentinels stalk the Earth, and the X-Men are humanity's only hope...until they die! Also featuring the first appearance of Alpha Flight, the return of the Wendigo, the history of the X-Men from Cyclops himself...and a demon for Christmas!? "},
    {"title": "Batman: The Dark Knight Returns", "publisher": "DC Comics", "issue_number": "#1", "cover_path": "dark_knight_returns.jpg", "writers": ["Frank Miller"], "artists": ["Frank Miller", "Klaus Janson", "Lynn Varley"], "description": "The Dark Knight Returns (alternatively titled Batman: The Dark Knight Returns) is a 1986 four-issue comic book miniseries starring Batman, written by Frank Miller, illustrated by Miller and Klaus Janson, and published by DC Comics. When the series was collected into a single volume later that year, the story title for the first issue was applied to the entire series. The Dark Knight Returns tells an alternative story of Bruce Wayne, who at 55 years old returns from retirement to fight crime and faces opposition from the Gotham City police force and the United States government. The story introduces Carrie Kelley as the new Robin and culminates with a confrontation against Superman."},
    {"title": "All-Star Superman", "publisher": "DC Comics", "issue_number": "#1", "cover_path": "all-star-superman.jpg", "writers": ["Grant Morrison"], "artists": ["Frank Quitely", "Jamie Grant"], "description": "At a cultural moment of near-total Batman dominance, Grant Morrison and Frank Quitely released the defining Superman work of the new millennium: A 12-issue saga that weaves together the character's strange history into a mythic saga that deconstructs the Superman legend while hyperbolizing it into new, colorful directions."},
    {"title": "Batman: Year One", "publisher": "DC Comics", "issue_number": "#404", "cover_path": "batman-year-one.jpg", "writers": ["Frank Miller"], "artists": ["David Mazzucchelli", "Richmond Lewis"], "description": "Year One is a Batman storyline written by Frank Miller with illustrations by Dave Mazzucchelli. It was published in 1987 through the Batman series, as a new origin story for the character. This is one of many Post-Crisis reboots, establishing the DCU's history following Crisis on Infinite Earths. It's considered to be the first canon Batman story in New Earth continuity."},
    {"title": "Crisis on Infinite Earths", "publisher": "DC Comics", "issue_number": "#1", "cover_path": "crisis-on-infinite-earths.jpg", "writers": ["Marv Wolfman", "Robert Greenberger"], "artists": ["George Perez", "Dick Giordano", "Anthony Tollin"], "description": "This is the story that changed the DC Universe forever. A mysterious being known as the Anti-Monitor has begun a crusade across time to bring about the end of all existence. As alternate earths are systematically destroyed, the Monitor quickly assembles a team of super-heroes from across time and space to battle his counterpart and stop the destruction. DC's greatest heroes including Superman, Batman, Wonder Woman, Green Lantern, and Aquaman, assemble to stop the menace, but as they watch both the Flash and Supergirl die in battle, they begin to wonder if even all of the heroes in the world can stop this destructive force."},
    {"title": "Kingdom Come", "publisher": "DC Comics", "issue_number": "#1", "cover_path": "kingdom-come.jpg", "writers": ["Mark Waid"], "artists": ["Alex Ross"], "description": "Kingdom Come was a four-issue limited series published from May until August of 1996 under DC's Elseworlds imprint. Like all Elseworlds, this series was set in an alternate reality outside that of the mainstream DC Universe. The series was written by Mark Waid with fully painted illustrations and covers by Alex Ross. All four issues were collected in both softcover and hardcover editions as well as a slipcase Absolute Edition."},
    {"title": "DC: The New Frontier", "publisher": "DC Comics", "issue_number": "#1", "cover_path": "dc-the-new-frontier.jpg", "writers": ["Darwyn Cooke"], "artists": ["Dave Stewart"], "description": "Takes readers on an epic journey from the end of the Golden Age to the genesis of a bold new era for the super-hero, recounting the dawning of the DC Universe's Silver Age from the perspective of those brave individuals who made it happen."},
    {"title": "The Judas Contract: Book One - The Eyes of Tara Markov!", "publisher": "DC Comics", "issue_number": "#42", "cover_path": "new-teen-titans-judas.jpg", "writers": ["Mark Wolfman"], "artists": ["George Perez", "Dick Giordano", "Adrienne Roy"], "description": "Donna and Kory finish up a photo shoot at Donna's studio. Gar, naturally, is overwhelmed by the skimpiness of Kory's bathing suit. Tara is present, and asks how Donna could afford such an expansive studio apartment. Donna tells her that it was a gift from Queen Hippolyta. What none of the Titans present realize is that someone is surreptitiously taking surveillance photos of Donna's studio...."},
    {"title": "Batman: The Killing Joke", "publisher": "DC Comics", "issue_number": "#42", "cover_path": "batman-killing-joke.JPG", "writers": ["Alan Moore"], "artists": ["Brian Bolland"], "description": "Batman: The Killing Joke is an influential one-shot superhero comic book written by Alan Moore and drawn by Brian Bolland, published by DC Comics in 1988. It has in its original form continuously been held in print since then. It has also been reprinted as part of the DC Universe: The Stories of Alan Moore-trade paperback."},
    {"title": "Superman: Whatever Happened to the Man of Tomorrow?", "publisher": "DC Comics", "issue_number": "#423", "cover_path": "superman-what-happened.jpg", "writers": ["Alan Moore"], "artists": ["Curt Swan", "George Perez", "Kurt Schaffenberger"], "description": "\"Whatever Happened to the Man of Tomorrow?\" is a 1986 comic book story featuring the DC Comics character of Superman. Written by Alan Moore with help from long-time Superman editor, Julius Schwartz, the story was published in two parts, beginning in Superman #423 and ending in Action Comics #583, both published in September 1986. The story was drawn by long-time artist Curt Swan, in his final major contribution to the Superman titles, and was inked by George Pérez in the issue of Superman and Kurt Schaffenberger in the issue of Action Comics. The story was an imaginary tale which told the final story of the Silver Age Superman and his long history,[1] which was being rebooted following the events of Crisis on Infinite Earths, before his modern introduction in the John Byrne series, The Man of Steel."},
    {"title": "The Man of Steel", "publisher": "DC Comics", "issue_number": "#1", "cover_path": "the-man-of-steel.png", "writers": ["John Byrne"], "artists": ["John Byrne", "Dick Giordano", "John Costanza"], "description": "The Man of Steel is a 1986 comic book limited series featuring the DC Comics character Superman. Written and drawn by John Byrne, the series was presented in six issues which were inked by Dick Giordano. The series told the story of Superman's modern origin, which had been rebooted following the 1986 series Crisis on Infinite Earths."},
    {"title": "Snowbirds Don't Fly", "publisher": "DC Comics", "issue_number": "#85", "cover_path": "green-lantern.jpg", "writers": ["Dennis O'Neil"], "artists": ["Neil Adams", "Dick Giordano"], "description": "In the first part (Green Lantern/Green Arrow #85), Green Arrow (Oliver Queen) runs into muggers who shoot him with a crossbow. Strangely, the weapon is loaded with his own arrows. Tracking down the attackers, Green Arrow and his best friend, Green Lantern Hal Jordan, find out that the muggers are junkies who need money for their addiction, and are surprised to find Queen's ward Speedy (Roy Harper) among them. They think he is working undercover to bust the junkies, but Queen catches him red-handed when he tries to shoot heroin. It becomes evident that the stolen arrows are indeed Queen's, which he shares with Harper when they fight crime together. In the second part (Green Lantern/Green Arrow #86), an enraged Green Arrow lashes out at his ward. In shame, Harper withdraws cold turkey, and one of the junkies dies of a drug overdose. Queen and Lantern tackle the kingpin of the drug ring, a pharmaceutics CEO who outwardly condemns drug abuse, and visit the funeral for the dead junkie."},
    {"title": "Arkham Asylum: A Serious House on Serious Earth", "publisher": "DC Comics", "issue_number": "#42", "cover_path": "arkham.jpg", "writers": ["Grant Morrison"], "artists": ["Dave McKean"], "description": "Arkham Asylum: A Serious House on Serious Earth (often shortened to Batman: Arkham Asylum) is a Batman graphic novel written by Grant Morrison and illustrated by Dave McKean. It was originally published in the United States in both hardcover and softcover editions by DC Comics in 1989. The subtitle is taken from Philip Larkin's poem \"Church Going.\""},
    ]

if db(db.comicbox.id > 0).count() <6:

    for i in range(0, 10):
        db.comicbox.insert(user_id=i, name='Box A', private=False if random.randint(0,1)==1 else True)
        db.comicbox.insert(user_id=i, name='Box B', private=False if random.randint(0,1)==1 else True)
        db.comicbox.insert(user_id=i, name='Box C', private=False if random.randint(0,1)==1 else True)
        db.comicbox.insert(user_id=i, name='Box D', private=False if random.randint(0,1)==1 else True)
        db.comicbox.insert(user_id=i, name='Box E', private=False if random.randint(0,1)==1 else True)
        db.comicbox.insert(user_id=i, name='Box F', private=False if random.randint(0,1)==1 else True)

    for c in range(0, 250):
        i = random.randint(1, 24)
        for x in range(1, random.randint(0, len(templateComics)-1)):
            comic = templateComics[x]
            user_id = db(db.comicbox.id == i).select(db.comicbox.user_id).column()[0]
            # Insert publisher
            if len(db((db.publisher.name == comic['publisher']) & (db.publisher.user_id == user_id)).select())==0:
                publisher_id = db.publisher.insert(user_id=user_id, name=comic['publisher'])
            else:
                publisher_id = db((db.publisher.name == comic['publisher']) & (db.publisher.user_id == user_id)).select(db.publisher.id).column()[0]

            comicId = db.comicbook.insert(box_id=i, title=comic['title'], publisher=publisher_id,
                                        issue_number=comic['issue_number'], description=comic['description'],
                                        cover=open(os.path.join(os.path.dirname(__file__), '../static/default_covers/'+comic['cover_path'])))
            for artist in comic['artists']:
                if len(db((db.artist.name==artist) & (db.artist.user_id==user_id)).select())==0:
                    artist_id = db.artist.insert(user_id=user_id, name=artist)
                else:
                    artist_id = db((db.artist.name==artist) & (db.artist.user_id==user_id)).select(db.artist.id).column()[0]
                db.comicArtist.insert(comicbook_id=comicId, artist_id=artist_id)

            for writer in comic['writers']:
                if len(db((db.writer.name==writer) & (db.writer.user_id==user_id)).select())==0:
                    writer_id = db.writer.insert(user_id=user_id, name=writer)
                else:
                    writer_id = db((db.writer.name==writer) & (db.writer.user_id==user_id)).select(db.writer.id).column()[0]
                db.comicWriter.insert(comicbook_id=comicId, writer_id=writer_id)
