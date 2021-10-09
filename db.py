import sqlite3

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

if __name__ == '__main__':
    conn = get_connection()
    create_files_table_if_not_exist(conn)