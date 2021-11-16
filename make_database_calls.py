import psycopg2
import os
import traceback
source_conn = None


def log_err(errmsg):
    """
    This method is used for error response
    :param errmsg:
    :return:
    """
    print(errmsg)
    return {
        "body": errmsg,
        "headers": {},
        "statusCode": 400,
        "isBase64Encoded": "false",
    }


def make_source_connection():
    """
    This method is used make connection to RDS DB
    :param connection_string:
    :return:
    """
    global source_conn
    conn_str = os.environ.get('DATABASE_URL')
    try:
        if source_conn is None:
            print("Opening Source Connection")
            source_conn = psycopg2.connect(conn_str, sslmode='require')
            source_conn.autocommit = True
        else:
            print("Source Connection already open")
    except:
        return log_err(
            "ERROR: Cannot connect to database from handler.\n{}".format(
                traceback.format_exc()
            )
        )

    return source_conn


def fetch_data(conn, query, parameters):
    result = []
    print("Now executing: %s %s" % (query, parameters))
    rowcount = 0
    try:
        cursor = conn.cursor()
        if parameters is not None:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        print(f'Cursor description and rownumber, {cursor.description}, {cursor.rowcount}')

        rowcount = cursor.rowcount
        if cursor.description is not None:
            raw = cursor.fetchall()
            for line in raw:
                result.append(line)
        return result, rowcount

    except:
        raise Exception("ERROR: Cannot execute cursor.\n{}".format(
            traceback.format_exc()))
    finally:
        cursor.close()
