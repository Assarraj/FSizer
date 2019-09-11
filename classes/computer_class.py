from wmi import WMI


class Computer:
    def __init__(self):
        self.myWMI = WMI()

    def get_computer_name(self):
        return self.myWMI.Win32_ComputerSystem()[0].Caption

    def get_domain_name(self):
        return self.myWMI.Win32_ComputerSystem()[0].Domain

    def get_computer_model(self):
        return self.myWMI.Win32_ComputerSystem()[0].Model

    def get_local_logical_disks_information(self):
        table = []

        logical_information = self.myWMI.Win32_LogicalDisk()

        for item in logical_information:
            row = {}
            if item.MediaType == 12:
                row["Drive Letter"] = item.DeviceID
                row["Total Size"] = item.Size
                row["Free Space"] = item.FreeSpace
                row["Free %"] = (int(item.FreeSpace)/int(item.Size)) * 100

            table.append(row)

        return table

    def get_shared_paths(self):
        table = []

        shares = self.myWMI.Win32_Share()

        for item in shares:
            row = {}
            if item.Type == 0:
                row["Path"] = item.Path
                row["Name"] = item.Name
                if item.Description == "":
                    row["Description"] = "-"
                else:
                    row["Description"] = item.Description

            if len(row) != 0:
                table.append(row)

        return table

