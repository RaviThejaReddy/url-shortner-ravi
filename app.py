from flask import Flask, request, redirect
import make_database_calls
import constants
import psycopg2
import json
import uuid

app = Flask(__name__)
con = make_database_calls.make_source_connection()


@app.route("/")
def home():
    response, rowcount = make_database_calls.fetch_data(con, 'select * from short_url', None)
    print(f'data in table short_url {response}')
    print(f'rows in table short_url {rowcount}')
    return str(response)


@app.route("/get_short_url")
def make_short_url():
    base_url = request.host_url
    long_url = json.loads(request.data)['url']
    response, rowcount = make_database_calls.fetch_data(con, constants.check_if_log_url_is_already_present, (long_url,))
    print(
        f'this url {long_url} is  {f"already present with short url {response[0][0]}" if rowcount else "not present"}')
    if not rowcount:
        response, rowcount = make_database_calls.fetch_data(con, constants.make_short_url, (long_url, uuid.uuid4().hex))
        print(response)
        print(rowcount)
    response, rowcount = make_database_calls.fetch_data(con, constants.check_if_log_url_is_already_present, (long_url,))
    return base_url+str(response[0][0])


@app.route("/<short_url>")
def get_long_url(short_url):
    response_long_url, rowcount = make_database_calls.fetch_data(con, constants.get_long_url, (short_url,))
    if rowcount:
        total_hits = int(response_long_url[0][1]) + 1
        response, rowcount = make_database_calls.fetch_data(con, constants.insert_into_hit_time_data,
                                                            (short_url,))
        response, rowcount = make_database_calls.fetch_data(con, constants.update_total_hits,
                                                            (str(total_hits), short_url))
        response, rowcount = make_database_calls.fetch_data(con, constants.get_total_hits_in_last_hour,
                                                            (short_url,))
        print(f'the long url for {short_url} is {response_long_url[0][0]} with total hits {total_hits}')
        data = {'long_url': response_long_url[0][0],
                'total_hits': total_hits,
                'total_hits_in_last_hour': response[0]}
        return data


@app.route("/search/<keypharse>")
def search_long_url(keypharse):
    response, rowcount = make_database_calls.fetch_data(con, constants.search_long_url, ('%' + keypharse + '%',))
    if rowcount:
        print(f'matching urls are {response}')
        return str(response)


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()
