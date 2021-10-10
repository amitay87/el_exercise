import sqlite3

# TODO: add exception handling

# TODO: refactor to a class with connection as an attribute (state) (singleton?)
class DBManager():
    def __enter__(self):
        self.conn = sqlite3.connect('meetings.db')
        self._create_files_table_if_not_exist()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def _create_files_table_if_not_exist(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS Files 
                        (
                           ID INT PRIMARY KEY     , 
                           MEETING_UUID           TEXT    , 
                           CALCULATED_HASH            TEXT    
                        )
                    '''
                     )

        print("Table created successfully")

    def insert_meeting_file(self, meeting_uuid, calculated_hash):
        # TODO: sanitize input - Done
        # TODO: handle edge case of duplicated UUID
        # meeting_uuid = meeting_uuid.replace('-','')
        query = f'''
        INSERT INTO Files (meeting_uuid, calculated_hash)
        VALUES( ?,	?);
        '''

        self.conn.execute(query, (meeting_uuid, calculated_hash))
        self.conn.commit()

    def get_calculated_hash(self, meeting_uuid):
        query = f'''
            SELECT calculated_hash
            FROM Files
            WHERE meeting_uuid = ?;
        '''

        cur = self.conn.cursor()
        cur.execute(query, (meeting_uuid, ))

        rows = cur.fetchall()
        print(f"AAA len(rows): {len(rows)}")
        if len(rows) > 0:
            return rows[0][0]
        # for row in rows:
        #     print(f"AAA  row: {row}")
        #     return row[0]



if __name__ == '__main__':
    pass
    # conn = get_connection()
    # create_files_table_if_not_exist(conn)