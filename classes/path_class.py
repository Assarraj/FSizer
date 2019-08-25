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
        myDB = Storage()
        start = time.time()
        full_size = 0

        for folderName, subfolders, filenames in os.walk(path):
            for filename in filenames:
                try:
                    full_size = full_size + os.path.getsize(folderName + "\\" + filename)
                except OSError as ee:
                    print(ee)
        end = time.time()

        lastID = myDB.DB_AddSize(self.GetPathID(path),
                                 round(time.time()),
                                 full_size,
                                 end-start)

        return full_size, lastID


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

    def RemovePath(self, path):
        myDB = Storage()
        myDB.DB_RemovePath(self.GetPathID(path))

    def GetMaxSize(self, path):
        myDB = Storage()
        return myDB.DB_GetMaxSize(self.GetPathID(path))

    def Get_QueryID_ByDate(self, firstDate, secondDate):
        myDB = Storage()
        firstDate_DateObj = datetime.datetime.strptime(firstDate, '%Y-%m-%d')
        secondDate_DateObj = datetime.datetime.strptime(secondDate, '%Y-%m-%d')

        results = myDB.DB_GetQueryID_ByDate(firstDate_DateObj, secondDate_DateObj)

    def calculate_files_suffix(self, path, query_ID):
        myDB =Storage()
        stat_count = {}
        stat_size = {}

        for root, sub, files in os.walk(path):
            for file in files:
                suffix = os.path.splitext(os.path.join(root, file))[1]
                suffix = suffix.replace('.', '')
                stat_count.setdefault(suffix, 0)
                stat_count[suffix] = stat_count[suffix] + 1

                stat_size.setdefault(suffix, 0)
                stat_size[suffix] = stat_size[suffix] + os.path.getsize(os.path.join(root, file))

        for key in stat_count.keys():
            if self.is_FE_Exist(key) is True:
                myDB.DB_AddSuffixCountSize(query_ID,
                                           myDB.DB_GetFE_ID(key),
                                           stat_count[key],
                                           stat_size[key])
            else:
                myDB.DB_AddSuffixCountSize(query_ID,
                                           myDB.DB_AddUnkownFE(key),
                                           stat_count[key],
                                           stat_size[key])

    def is_FE_Exist(self, FE_Name):
        myDB = Storage()
        if myDB.DB_GetFE_ID(FE_Name) is not None:
            return True
        else:
            return False




