import sqlite3

# TODO: add exception handling

# TODO: refactor to a class with connection as an attribute (state)
def get_connection():
    conn = sqlite3.connect('meetings.db')
    print("Opened database successfully")
    return conn

def create_files_table_if_not_exist(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS Files 
                    (
                       ID INT PRIMARY KEY     , 
                       MEETING_UUID           TEXT    , 
                       CALCULATED_HASH            TEXT    
                    )
                '''
                 )

    print("Table created successfully")

def insert_meeting_file(conn, meeting_uuid, calculated_hash):
    # TODO: sanitize input
    # meeting_uuid = meeting_uuid.replace('-','')
    query = f'''
    INSERT INTO Files (meeting_uuid, calculated_hash)
    VALUES( ?,	?);
    '''

    conn.execute(query, (meeting_uuid, calculated_hash))
    conn.commit()

    # conn.close()


def get_calculated_hash(conn, meeting_uuid):
    query = f'''
        SELECT calculated_hash
        FROM Files
        WHERE meeting_uuid = ?;
    '''
    print(f"AAA query: {query}")
    print(f"AAA meeting_uuid: {meeting_uuid}")
    cur = conn.cursor()
    cur.execute(query, (meeting_uuid, ))

    rows = cur.fetchall()
    print(f"AAA len(rows): {len(rows)}")
    for row in rows:
        print(row)
        return row



if __name__ == '__main__':
    conn = get_connection()
    create_files_table_if_not_exist(conn)