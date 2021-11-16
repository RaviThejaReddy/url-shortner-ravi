from flask import Flask
from make_database_connection import make_connection
import constants

app = Flask(__name__)


@app.route("/")
def home():
    response = []
    cur, con = make_connection()
    for x in constants.tables:
        res = cur.execute(x)
        response.append(res)
    cur.close()
    con.commit()
    return response


# @app.route("/get_short_url/")
# def get_short_url():
#     pass
#
#
# def search_for_url():
#     pass
#

if __name__ == "__main__":
    app.run()
