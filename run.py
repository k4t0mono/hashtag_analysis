from subprocess import run


if __name__ == "__main__":
    with open('hashtags') as fl:
        lns = fl.readlines()
        hashtags = [ tuple(ln.split()) for ln in lns ]

    for (db, ht) in hashtags:
        run(('python', 'create_db.py', db, ht))
        run(('python', 'main.py', db, ht))