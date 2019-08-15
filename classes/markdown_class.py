import os
import datetime


class MarkDown:
    default_path = ".\\report"

    def __init__(self):
        self.__datetime = datetime.datetime.now()
        self.__filename = self.__MD_filename(self.__datetime)
        self.__foldername = self.__MD_foldername(self.__datetime)
        self.__reportpath = os.path.join(self.default_path, self.__foldername)

        # Create a folder with the new name
        os.mkdir(self.__reportpath)

        self.__file_handler = open(os.path.join(self.__reportpath, self.__filename), "w+")

    def MD_getFilename(self):
        return self.__filename

    def MD_getFoldername(self):
        return self.__foldername

    def MD_getReportpath(self):
        return self.__reportpath

    def MD_header(self, level, text):
        self.__file_handler.write("{0} {1}\r\n".format("#" * level, text))

    def __MD_is_exist(self, path):
        return os.path.exists(path)

    def __MD_filename(self, dt):
        return "report - ({0}-{1}-{2} {3}-{4}-{5}).md".format(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

    def __MD_foldername(self, dt):
        return "report - ({0}-{1}-{2} {3}-{4}-{5})".format(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

    def MD_text(self, text, newline=False):
        if newline is False:
            self.__file_handler.write("{0}".format(text))
        else:
            self.__file_handler.write("{0}\r\n".format(text))

    def MD_image(self, text, url, newline=False):
        if newline is False:
            self.__file_handler.write("![{0}]({1})".format(text, url))
        else:
            self.__file_handler.write("![{0}]({1})\r\n".format(text, url))

    def MD_link(self, text, url, newline=False):
        if newline is False:
            self.__file_handler.write("[{0}]({1})".format(text, url))
        else:
            self.__file_handler.write("[{0}]({1})\r\n".format(text, url))

    def MD_newline(self):
        self.__file_handler.write("\r\n")

    def MD_horizontal_rule(self):
        self.__file_handler.write("------\r\n")

    def MD_table(self, content):
        table = ""
        for ID, row in enumerate(content):
            cont = []
            header = []
            linebreacker = []

            for key in row.keys():
                # Print the Header
                header.append(key)
                linebreacker.append("---")

            for item in row.values():
                cont.append(str(item))

            if ID == 0:
                table = table + "{0}\n{1}\n".format(
                    ' | '.join(header),
                    ' | '.join(linebreacker)
                )

            table = table + "{0}\n".format(
                ' | '.join(cont)
            )

        self.__file_handler.write(table)

    def MD_commit(self):
        self.__file_handler.close()

