from classes.path_class import Path
from classes.unitconvertor import UniConv
from matplotlib import pyplot as plt
from time import time
import os
import random


class Report:

    def RP_MainTable(self, path):
        myPath = Path(path)
        sizes = myPath.GetSizes(2)
        myUnit = UniConv()

        row = {'ID': myPath.pathID,
               'Path': myPath.path}

        for size in sizes:
            row[str(size['time_stamp'])] = myUnit.beauty_size(size['size'])

        if len(sizes) > 1:
            if self.__RP_CompareSizes(sizes[0]['size'], sizes[1]['size']) == 1:
                row['State'] = "Decrease"
            elif self.__RP_CompareSizes(sizes[0]['size'], sizes[1]['size']) == 2:
                row['State'] = "Increase"
            elif self.__RP_CompareSizes(sizes[0]['size'], sizes[1]['size']) == 0:
                row['State'] = "The same"
        else:
            row['State'] = "=="

        return row

    def __RP_CompareSizes(self, old, new):
        if old > new:
            return 1
        elif old < new:
            return 2
        elif old == new:
            return 0

    def RP_DrawFig(self, path, reportName, reportPath):
        myPath = Path(path)
        myUnit = UniConv()

        unit = myUnit.max_unit(myPath.maxSize)

        timeStamp = []
        sizeList = []
        for size in myPath.GetSizes(0):
            timeStamp.append(size['time_stamp'])
            sizeList.append(myUnit.select_size(size['size'], unit))

        plt.title(path)

        plt.plot(timeStamp, sizeList,
                 marker='o', markerfacecolor='blue',
                 markersize=12, color='skyblue',
                 linewidth=4)

        plt.xlabel("Date")
        plt.ylabel("Size " + myUnit.get_unit_name(unit))

        plt.grid(True)

        filename = reportName + "_" + str(round(time() + random.random()*10000)) + ".png"
        plt.savefig(os.path.join(reportPath,filename),
                    format="png",
                    dpi=300)
        plt.close()

        return filename
