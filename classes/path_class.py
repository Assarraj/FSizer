import os
import time, datetime
from classes.database_class import Storage


class Path:
    def __init__(self, path):
        self.myDB = Storage()

        self.path = path
        self.pathID = self.myDB.DB_GetPathID(path)
        try:
            self.size, self.calculationTime = self.__CalculateSize(self.path)
        except:
            print("Error with calculation of size ")
        self.sizeUnit = self.__beauty_size(self.size)
        self.maxSize = self.myDB.DB_GetMaxSize(self.pathID)


    def __CalculateSize(self, path):
        start = time.time()
        full_size = 0

        for folderName, subfolders, filenames in os.walk(path):
            for filename in filenames:
                try:
                    full_size = full_size + os.path.getsize(folderName + "\\" + filename)
                except OSError as ee:
                    print(ee)
        end = time.time()
        return full_size, end-start

    def __beauty_size(self, given_size):
        i = 0
        calc_size = given_size
        while True:
            if calc_size >= 1000:
                calc_size = calc_size / 1024
                i = i + 1
            else:
                break

        if i == 0:
            unit = "Bytes"
        elif i == 1:
            unit = "KBytes"
        elif i == 2:
            unit = "MBytes"
        elif i == 3:
            unit = "GBytes"
        elif i == 4:
            unit = "TBytes"
        elif i == 5:
            unit = "PBytes"
        elif i == 6:
            unit = "EBytes"

        return "{0:05.2f} {1}".format(calc_size, unit)

    def GetSizes(self, count=1):
        result_list = []

        results = self.myDB.DB_GetSize(self.pathID, count)

        for row in results:
            dt = datetime.datetime.fromtimestamp(row['time_stamp'])

            presentable_time = "{0:02d}:{1:02d} {2:02d}-{3:02d}-{4}".format(
                dt.hour, dt.minute, dt.day, dt.month, dt.year
            )

            result_list.append({'time_stamp': presentable_time,
                                'size': row['size']})

        return result_list

    def Commit(self):
        try:
            self.myDB.DB_AddSize(self.pathID, round(time.time()), self.size, self.calculationTime)
            return True
        except:
            return False

    def RemovePath(self):
        self.myDB.DB_RemovePath(self.pathID)

