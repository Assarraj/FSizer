import sqlite3


class Storage:
    DBPath = "files.db"

    def __init__(self):
        self.conn = sqlite3.connect(self.DBPath)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def DB_AddNewPath(self, path):
        self.cur.execute("""
        INSERT INTO paths (path) VALUES ('{0}');
        """.format(path))

        self.conn.commit()

    def DB_GetPathID(self, path):
        # Return the PATH ID
        result = self.cur.execute("""
        SELECT path_ID
        FROM paths
        WHERE UPPER(path)=UPPER('{0}');
        """.format(path)).fetchone()

        return result['path_ID']

    def DB_is_new(self, path):
        results = self.cur.execute("""
                SELECT * 
                FROM paths 
                WHERE UPPER(path) = UPPER('{0}');
                """.format(path)).fetchone()

        if results is None:
            return True
        else:
            return False

    def DB_AddSize(self, PathID, TimeStamp, Size, calculationTime):
        self.cur.execute("""
        INSERT INTO queries (path_ID, time_stamp, size, time_duration) 
        VALUES ({0}, {1}, {2}, {3});
        """.format(PathID, TimeStamp, Size, calculationTime))

        self.conn.commit()

        return self.cur.lastrowid

    def DB_GetSize(self, pathID, count, reverse=False):
        query = """
        SELECT queries.time_stamp, queries.size 
        FROM queries
        WHERE queries.path_ID = {0}
        ORDER BY queries.time_stamp
        """

        if reverse is True:
            query = query + " DESC"
        if count >= 1:
            query = query + " LIMIT {1}"

        query = query + ";"

        results = self.cur.execute(query.format(pathID, count)).fetchall()

        return results

    def DB_GetAllPaths(self):
        results = self.cur.execute("""
                    SELECT path 
                    FROM paths  
                    ORDER BY path_ID;
                    """).fetchall()

        return results

    def DB_RemovePath(self, pathID):
        self.cur.execute("""
        DELETE 
        FROM paths
        WHERE path_ID = {0} 
        """.format(pathID))

        self.cur.execute("""
        DELETE 
        FROM queries  
        WHERE path_ID = {0} 
        """.format(pathID))

        self.conn.commit()

    def DB_RemoveAllPath(self):
        self.cur.execute("""
        DELETE FROM paths;
        """)

        self.cur.execute("""
        DELETE FROM queries;
        """)

        self.conn.commit()

    def DB_GetMaxSize(self, pathID):
        results = self.cur.execute("""
                        SELECT MAX(queries.size)
                        AS max_size
                        FROM queries
                        WHERE queries.path_ID = {0};
                        """.format(pathID)).fetchone()

        return results['max_size']

    def DB_GetFEC_ID(self, FE_name):
        results = self.cur.execute("""
                                SELECT FEC_ID
                                FROM file_extensions
                                WHERE file_extensions.FE_Name = {0}
                                """.format(FE_name)).fetchone()
        return results['FEC_ID']

    def DB_GetFE_ID(self, FE_name):
        results = self.cur.execute("""
                                SELECT FE_ID
                                FROM file_extensions
                                WHERE file_extensions.FE_Name = {0}
                                """.format(FE_name)).fetchone()
        return results['FE_ID']

    def DB_AddSuffixCountSize(self, query_ID, FE_ID, count, size):
        self.cur.execute("""
        INSERT INTO query_file_extensions (
        query_ID, FE_ID, count, size
        ) 
        VALUES (
        {0}, {1}, {2}, {3}
        );
        """.format(query_ID, FE_ID, count, size))

        self.conn.commit()

    def DB_GetQueryID_ByDate(self, FirstDate , SecondDate):
        results = self.cur.execute("""
        SELECT queries.query_ID
        FROM queries
        WHERE DATE(queries.time_stamp, 'unixepoch') >= DATE({0})
        AND DATE(queries.time_stamp, 'unixepoch') <= DATE({1});
        """.format(FirstDate , SecondDate)).fetchall()

        return results

    def DB_GetAllDates(self):
        results = self.cur.execute("""
                SELECT DATE(queries.time_stamp, 'unixepoch') AS query_date
                FROM queries
                GROUP BY query_date;
                """).fetchall()

        return results

    def DB_GetDatesPerPath(self, pathID):
        results = self.cur.execute("""
                    SELECT DATE(queries.time_stamp, 'unixepoch') AS query_date
                    FROM queries
                    WHERE queries.path_ID = {0}
                    GROUP BY query_date;
                    """.format(pathID)).fetchall()
        return results

    def DB_AddFEC(self, FEC_Name, FEC_Info):
        self.cur.execute("""
                INSERT INTO file_extensions_category (
                FEC_Name, FEC_Info
                ) 
                VALUES (
                {0}, {1}
                );
                """.format(FEC_Name, FEC_Info))

        self.conn.commit()

    def DB_AddFE(self, FEC_ID, FE_Name):
        self.cur.execute("""
                INSERT INTO file_extensions (
                FEC_ID, FE_Name
                ) 
                VALUES (
                {0}, {1}
                );
                """.format(FEC_ID, FE_Name))

        self.conn.commit()

    def DB_RemoveFEC(self, FEC_ID):
        self.cur.execute("""
                DELETE FROM file_extensions_category
                WHERE file_extensions_category.FEC_ID = {0};
                """.format(FEC_ID))

        self.cur.execute("""
                        DELETE FROM file_extensions
                        WHERE file_extensions.FEC_ID = {0};
                        """.format(FEC_ID))

        self.conn.commit()

    def DB_RemoveFE(self, FE_ID):
        self.cur.execute("""
                        DELETE FROM file_extensions
                        WHERE file_extensions.FE_ID = {0};
                        """.format(FE_ID))

        self.conn.commit()

    def DB_GetAllFEC(self):
        results = self.cur.execute("""
        SELECT FEC_ID, FEC_Name, FEC_Info
        FROM file_extensions_category
        ORDER BY FEC_ID;
        """).fetchall()

        return results

    def DB_GetAllFE_ByFEC(self, FEC_ID):
        results = self.cur.execute("""
        SELECT FE_ID, FE_Name
        FROM file_extensions
        WHERE FEC_ID = {0}
        ORDER BY FE_Name;
        """.format(FEC_ID)).fetchall()

        return results

    def DB_GetFEC(self, FEC_ID):
        results = self.cur.execute("""
        SELECT FEC_Name, FEC_Info
        FROM file_extensions_category
        WHERE file_extensions_category.FEC_ID = {0};
        """.format(FEC_ID)).fetchall()

        return results

    def DB_GetFE_SizeCount(self, query_ID):
        results = self.cur.execute("""
        SELECT count, size
        FROM query_file_extensions
        WHERE query_file_extensions.query_ID = {0};
        """.format(query_ID)).fetchall()

        return results

    def DB_AddUnkownFE(self,FE_Name):
        self.cur.execute("""
                        INSERT INTO file_extensions (
                        FEC_ID, FE_Name
                        ) 
                        VALUES (
                        99, {0}
                        );
                        """.format(FE_Name))

        self.conn.commit()

        return self.cur.lastrowid

