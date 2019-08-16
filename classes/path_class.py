import os
import time
import datetime
from classes.database_class import Storage


class Path:
    def GetPathID(self, path):
        myDB = Storage()

        if myDB.DB_is_new(path) is True:
            return False
        else:
            return myDB.DB_GetPathID(path)

    def AddPath(self, path):
        myDB = Storage()

        if os.path.exists(path) is True:
            if myDB.DB_is_new(path) is True:
                myDB.DB_AddNewPath(path)
                return True
            else:
                return False
        else:
            return False

    def CalculateSize(self, path):
        start = time.time()
        full_size = 0

        for folderName, subfolders, filenames in os.walk(path):
            for filename in filenames:
                try:
                    full_size = full_size + os.path.getsize(folderName + "\\" + filename)
                except OSError as ee:
                    print(ee)
        end = time.time()

        return self.__Commit(path, full_size, end-start)

    def GetSizes(self, path, count=1, reverse=False):
        result_list = []
        myDB = Storage()

        results = myDB.DB_GetSize(self.GetPathID(path), count, reverse)

        for row in results:
            dt = datetime.datetime.fromtimestamp(row['time_stamp'])

            presentable_time = "{0:02d}-{1:02d}-{2}".format(
               dt.day, dt.month, dt.year
            )

            result_list.append({'time_stamp': presentable_time,
                                'size': row['size']})

        return result_list

    def __Commit(self, path, totalsize, calculationTime):
        myDB = Storage()
        try:
            myDB.DB_AddSize(self.GetPathID(path),
                            round(time.time()),
                            totalsize,
                            calculationTime)
            return True
        except:
            return False

    def RemovePath(self, path):
        myDB = Storage()
        myDB.DB_RemovePath(self.GetPathID(path))

    def GetMaxSize(self, path):
        myDB = Storage()
        return myDB.DB_GetMaxSize(self.GetPathID(path))



