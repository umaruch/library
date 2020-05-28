from sys import argv
from app import app
from config import DEBUG, HOST, PORT
from app.db_create import drop_table, db_test


def help():
    print("'runserver' - run flask app")
    print("'droptable' - drop table")
    print("'dbtest' - add test values from table")
    print("За дальнейшими разьяснениями можете отправляться на хуй")


try:
    if argv[1] == "runserver":
        app.run(
            debug = True,
            host = HOST,
            port = PORT
            )
    elif argv[1] == "droptable":
        drop_table()
    elif argv[1] == "dbtest":
        db_test()
    else:
        help()
except IndexError:
    help()