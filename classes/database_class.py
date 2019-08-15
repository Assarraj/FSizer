import sqlite3


class Storage:
    DBPath = "files.db"

    def __init__(self):
        self.conn = sqlite3.connect(self.DBPath)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def DB_GetPathID(self, path):
        """Will return the path ID and add it to the DB if it's new path"""

        # Check is it new then add it to DB
        if self.DB_is_new(path) is True:
            self.cur.execute("""
            INSERT INTO paths (path) VALUES ('{0}');
            """.format(path))

            self.conn.commit()

        # Return the PATH ID
        result = self.cur.execute("""
        SELECT path_ID FROM 'paths' WHERE UPPER(path)=UPPER('{0}');
        """.format(path)).fetchone()

        return result['path_ID']

    def DB_is_new(self, path):
        results = self.cur.execute("""
                SELECT * FROM 'paths' 
                WHERE UPPER(path) = UPPER('{0}');
                """.format(path)).fetchone()

        if results is None:
            return True
        else:
            return False

    def DB_AddSize(self, PathID, TimeStamp, Size, calculationTime):
        self.cur.execute("""
        INSERT INTO size (path_ID, time_stamp, size, time_duration) 
        VALUES ({0}, {1}, {2}, {3});
        """.format(PathID, TimeStamp, Size, calculationTime))

        self.conn.commit()

    def DB_GetSize(self, pathID, count):
        if count >= 1:
            results = self.cur.execute("""
            SELECT time_stamp, size 
            FROM 'size' 
            WHERE path_ID = {0}
            ORDER BY time_stamp 
            LIMIT {1};
            """.format(pathID, count)).fetchall()
        elif count < 1:
            results = self.cur.execute("""
            SELECT time_stamp, size 
            FROM 'size' 
            WHERE path_ID = {0} 
            ORDER BY time_stamp;
            """.format(pathID)).fetchall()

        return results

    def DB_GetAllPaths(self):
        results = self.cur.execute("""
                    SELECT path 
                    FROM 'paths'  
                    ORDER BY path_ID;
                    """).fetchall()

        list_results = []

        for row in results:
            list_results.append(row['path'])

        return list_results

    def DB_RemovePath(self, pathID):
        results = self.cur.execute("""
                    DELETE 
                    FROM 'paths'  
                    WHERE path_ID = {0} 
                    """.format(pathID))
        results = self.cur.execute("""
                    DELETE 
                    FROM 'size'  
                    WHERE path_ID = {0} 
                    """.format(pathID))
        self.conn.commit()


    def DB_RemoveAllPath(self):
        results = self.cur.execute("""
                    DELETE 
                    FROM 'paths';   
                    """)
        results = self.cur.execute("""
                    DELETE 
                    FROM 'size';   
                    """)
        self.conn.commit()

    def DB_GetMaxSize(self, pathID):
        results = self.cur.execute("""
                        SELECT MAX(size.size)
                        AS 'max_size'
                        FROM size
                        WHERE size.path_ID = {0};
                        """.format(pathID)).fetchone()

        return results['max_size']
