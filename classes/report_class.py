from classes.path_class import Path
from classes.database_class import Storage
from classes.unitconvertor import UniConv
from classes.computer_class import Computer
from matplotlib import pyplot as plt
from time import time
import os
import random
import wmi


class Report:

    def __init__(self):
        self.myDB = Storage()
        self.myUnit = UniConv()
        self.myWMI = wmi.WMI()

    def get_pc_information(self):
        table = []

        table.append({"Item": "Computer Name",
                      "Value": self.myWMI.Win32_ComputerSystem()[0].Caption})
        table.append({"Item": "Domain Name",
                      "Value": self.myWMI.Win32_ComputerSystem()[0].Domain})
        table.append({"Item": "Computer Model",
                      "Value": self.myWMI.Win32_ComputerSystem()[0].Model})

        return table

    def get_logical_disk(self):
        table = []

        logical_information = self.myWMI.Win32_LogicalDisk()

        for item in logical_information:
            row = {}
            if item.MediaType == 12:
                row["Drive Letter"] = item.DeviceID

                unit = self.myUnit.max_unit(int(item.Size))
                unit_name = self.myUnit.get_unit_name(unit)

                total_size = "{0} {1}".format(round(self.myUnit.select_size(int(item.Size), unit), 2), unit_name)
                free_space = "{0} {1}".format(round(self.myUnit.select_size(int(item.FreeSpace), unit), 2), unit_name)
                free_perc = "{0} %".format(round((int(item.FreeSpace)/int(item.Size)) * 100, 2))

                row["Total Size"] = total_size
                row["Free Space"] = free_space
                row["Free %"] = free_perc

            table.append(row)

        return table

    def get_growth(self, duration):
        table = []
        results = self.myDB.DB_GetSumSize_ByDate(duration)
        sizes = []
        for item in results:
            sizes.append(item["size"])

        unit_value = self.myUnit.max_unit(sizes)

        for item in results:
            row = {}
            row["Date"] = item["time_stamp"]
            row["Size"] = round(self.myUnit.select_size(item["size"]), unit_value)
            table.append(row)

        return table, self.myUnit.get_unit_name(unit_value)

    def draw_growth(self, table, unit_name,  report_path, basename):
        x = []
        y = []
        for row in table:
            x.append(row["Date"])
            y.append(row["Size"])

        plt.ylim(min(y) - 5, max(y) + 5)

        plt.plot(x,
                 y,
                 marker='o',
                 markerfacecolor='blue',
                 markersize=5,
                 color='skyblue',
                 linewidth=1, )

        plt.xlabel("Date")
        plt.ylabel("Size " + unit_name)

        plt.xticks(rotation=60)

        plt.grid(True)

        filename = basename + "_" + str(round(time() + random.random() * 10000)) + ".png"

        plt.savefig(os.path.join(report_path, filename),
                    format="png",
                    dpi=300,
                    bbox_inches='tight')
        plt.close()

        return filename

    def shared_paths_information(self, duration):
        table = []
        myPath = Path()
        paths = self.myDB.DB_GetAllPaths()

        for path in paths:
            row = {}
            sizes = self.myDB.DB_GetPathSizes_ByDate(myPath.GetPathID(path['path']), duration)

            row['Shared Path'] = path['path']

            lst = []
            for size in sizes:
                lst.append(size['size'])
            unit = self.myUnit.max_unit(lst)
            unit_name = self.myUnit.get_unit_name(unit)

            for size in sizes:
                row[str(size['time_stamp'])] = "{0} {1}".format(round(self.myUnit.select_size(size['size'], unit), 2), unit_name)

            table.append(row)

        return table


    def actual_shared_paths(self):
        myComputer = Computer()
        shared = myComputer.get_shared_paths()

        for item in shared:
            if self.myDB.DB_is_new(item['Path']) is not True:
                item['DB'] = ":heavy_check_mark:"
            else:
                item['DB'] = ":x:"

        return shared





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












