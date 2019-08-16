from classes.path_class import Path
from classes.markdown_class import MarkDown
from classes.database_class import Storage
from classes.unitconvertor import UniConv
from matplotlib import pyplot as plt
from time import time
import os
import random


class Report:

    def __init__(self):
        self.myMD = MarkDown()
        self.myDB = Storage()
        self.myUnit = UniConv()

    def RP_InsertIndex(self):
        self.myMD.MD_header(1, 'Index')
        self.myMD.MD_text('[toc]', True)
        self.myMD.MD_horizontal_rule()

    def RP_InsertSharedPaths(self):
        self.myMD.MD_header(1, 'Shared Paths')
        rows = self.myDB.DB_GetAllPaths()

        table = []

        for row in rows:
            table.append(self.__RP_MainTable(row['path']))

        self.myMD.MD_table(table)
        self.myMD.MD_horizontal_rule()

    def RP_InsertMoreInormation(self):
        self.myMD.MD_header(1, "More Information for each Path")
        paths = self.myDB.DB_GetAllPaths()

        for path in paths:
            filename = self.__RP_DrawFig(path['path'])
            self.myMD.MD_header(2, path['path'])
            self.myMD.MD_image('', filename, newline=True)

    def __RP_MainTable(self, path):
        myPath = Path()
        sizes = myPath.GetSizes(path, 2, True)

        row = {'ID': myPath.GetPathID(path),
               'Path': path}

        for size in sizes:
            row[str(size['time_stamp'])] = self.myUnit.beauty_size(size['size'])

        if len(sizes) > 1:
            row['State'] = self.__RP_CompareSizes(sizes[1]['size'], sizes[0]['size'])
        else:
            row['State'] = "=="

        return row

    def __RP_CompareSizes(self, old, new):
        if old > new:
            return "Decrease"
        elif old < new:
            return "Increase"
        elif old == new:
            return "The same"

    def __RP_DrawFig(self, path):
        myPath = Path()

        unit = self.myUnit.max_unit(myPath.GetMaxSize(path))

        timeStamp = []
        sizeList = []
        for size in myPath.GetSizes(path, 0):
            timeStamp.append(size['time_stamp'])
            sizeList.append(self.myUnit.select_size(size['size'], unit))

        plt.title(path)

        plt.plot(timeStamp, sizeList,
                 marker='o', markerfacecolor='blue',
                 markersize=12, color='skyblue',
                 linewidth=4)

        plt.xlabel("Date")
        plt.ylabel("Size " + self.myUnit.get_unit_name(unit))

        plt.grid(True)

        filename = self.myMD.MD_getFoldername() + "_" + str(round(time() + random.random()*10000)) + ".png"
        plt.savefig(os.path.join(self.myMD.MD_getReportpath(), filename),
                    format="png",
                    dpi=300)
        plt.close()

        return filename

    def RP_Commit(self):
        self.myMD.MD_commit()

