from classes.path_class import Path
from classes.markdown_class import MarkDown
from classes.database_class import Storage
from classes.unitconvertor import UniConv
from matplotlib import pyplot as plt
from time import time
import os
import random
import wmi


class Report:

    def __init__(self):
        self.myMD = MarkDown()
        self.myDB = Storage()
        self.myUnit = UniConv()
        self.myWMI = wmi.WMI()

        self.__base_file_name = self.myMD.MD_getFoldername()

    def get_pc_information(self):
        table = []
        table.append({"Item": "Computer Name",
                      "Value": self.myWMI.Win32_ComputerSystem()[0].Caption})
        table.append({"Item": "Domain Name",
                      "Value": self.myWMI.Win32_ComputerSystem()[0].Domain})
        table.append({"Item": "Computer Model",
                      "Value": self.myWMI.Win32_ComputerSystem()[0].Model})

        self.myMD.MD_table(table)
        self.myMD.MD_horizontal_rule()



    #------------------------------------

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
            sizeList.append(round(self.myUnit.select_size(size['size'], unit),2))

        plt.title(path)

        plt.plot(timeStamp,
                 sizeList,
                 marker='o',
                 markerfacecolor='blue',
                 markersize=5,
                 color='skyblue',
                 linewidth=1, )

        plt.xlabel("Date")
        plt.ylabel("Size " + self.myUnit.get_unit_name(unit))
        plt.xticks(rotation=60)

        plt.grid(True)

        filename = self.myMD.MD_getFoldername() + "_" + str(round(time() + random.random()*10000)) + ".png"

        plt.savefig(os.path.join(self.myMD.MD_getReportpath(), filename),
                    format="png",
                    dpi=300,
                    bbox_inches='tight')
        plt.close()

        return filename

    def RP_Commit(self):
        self.myMD.MD_commit()

    def RP_InsertFileTypes(self):
        self.myMD.MD_header(1, "File Type Information")

        for path in self.myDB.DB_GetAllPaths():
            myPath = Path()

            self.myMD.MD_header(2,"Biggest 10 files extensions inside " + path['path'])

            QueryID = self.myDB.DB_GetLastQueryID(myPath.GetPathID(path['path']))

            table = []

            for item in self.myDB.DB_GetQFE_ByQueryID(QueryID):
                table.append({"File Extension": self.myDB.DB_GetFEName(item['FE_ID']),
                              "Count": item['count'],
                              "Size": self.myUnit.beauty_size(item['size'])})

            self.myMD.MD_table(table)

    def RP_InsertPieChart_FEC_Size(self):
        self.myMD.MD_header(1, "File Type Graphs")

        for path in self.myDB.DB_GetAllPaths():
            myPath = Path()

            QueryID = self.myDB.DB_GetLastQueryID(myPath.GetPathID(path['path']))

            KeyItems = []
            ValueItems = []

            for FEC in self.myDB.DB_GetAllFEC():
                FEC_ID = FEC['FEC_ID']
                SumSize = self.myDB.DB_GetSumSize_ByFEC_QFE(FEC_ID, QueryID)
                KeyItems.append(FEC['FEC_Name'])
                ValueItems.append(SumSize)

                """
                if SumSize > 0:
                    KeyItems.append(FEC['FEC_Name'])
                    ValueItems.append(SumSize)
                """

            filename = self.__RP_Draw_BarChart(path['path'], KeyItems, ValueItems)

            self.myMD.MD_header(2, path['path'])
            if filename is not None:
                self.myMD.MD_image('', filename, newline=True)
            else:
                self.myMD.MD_text("This path is empty", True)


    def __RP_Draw_PieChart(self, path, KeyItems, ValueItems):
        plt.title(path)

        plt.pie(ValueItems,
                autopct='%1.0f',
                startangle=90,
                labeldistance=5.05)

        plt.axis('equal')
        plt.legend(KeyItems)

        filename = self.myMD.MD_getFoldername() + "_Pie_" + str(round(time() + random.random() * 10000)) + ".png"
        plt.savefig(os.path.join(self.myMD.MD_getReportpath(), filename),
                    format="png",
                    dpi=300)
        plt.close()

        return filename

    def __RP_Draw_BarChart(self, path, KeyItems, ValueItems):
        plt.title(path)

        ValueItems_Percent =[]
        ValueItems_Sum = sum(ValueItems)

        if ValueItems_Sum > 0:

            for item in ValueItems:
                ValueItems_Percent.append(round((item/ValueItems_Sum)*100))

            plt.ylabel("Percent")
            plt.ylim(0, 100)
            #plt.grid()
            plt.xticks(rotation=60)

            plt.bar(KeyItems,
                    ValueItems_Percent,
                    color=(0.1, 0.1, 0.1, 0.1),
                    edgecolor='blue')

            filename = self.myMD.MD_getFoldername() + "_Bar_" + str(round(time() + random.random() * 10000)) + ".png"
            plt.savefig(os.path.join(self.myMD.MD_getReportpath(), filename),
                        format="png",
                        dpi=300,
                        bbox_inches='tight')
            plt.close()

            return filename
        else:
            return None












