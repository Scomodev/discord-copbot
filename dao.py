import psycopg2
from os import environ

DATABASE_URL = environ.get('DATABASE_URL')

HELPEE_COUNT_QUERY = "SELECT COUNT(*) FROM entries WHERE helpee = %s GROUP BY helpee;"
HELPER_COUNT_QUERY = "SELECT COUNT(*) FROM entries WHERE helper = %s GROUP BY helper;"
INSERT_COPDOC_ENTRY_QUERY = "INSERT INTO entries(shoe, helper, helpee) VALUES(%s, %s, %s) RETURNING id;"
DELETE_COPDOC_ENTRY_QUERY = "DELETE FROM entries WHERE id = %s;"
GET_NUMBER_COPPED_BY_HELPER_QUERY = "SELECT helper, COUNT(*) FROM entries GROUP BY helper ORDER BY COUNT(*) DESC;"

conn = psycopg2.connect(DATABASE_URL, sslmode='require')


def delete_copdoc_entry(entry_id):
    cur = conn.cursor()
    cur.execute(DELETE_COPDOC_ENTRY_QUERY, ([entry_id]))
    conn.commit()
    cur.close()


def insert_new_copdoc_entry(shoe, helper, helpee):
    cur = conn.cursor()
    cur.execute(INSERT_COPDOC_ENTRY_QUERY,
                ([shoe, helper, helpee]))
    entry_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return entry_id


def get_helper_leader_board():
    cur = conn.cursor()
    cur.execute(GET_NUMBER_COPPED_BY_HELPER_QUERY)
    leader_board = cur.fetchall()
    print(leader_board)
    conn.commit()
    cur.close()
    return leader_board


def get_member_count_by_query_type(member_id, query):
    cur = conn.cursor()
    cur.execute(query, ([str(member_id)]))
    member_count = cur.fetchone()
    if member_count is None:
        member_count = 0
    else:
        member_count = member_count[0]
    conn.commit()
    cur.close()
    return int(member_count)
