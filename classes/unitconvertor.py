import datetime

class UniConv:

    def beauty_size(self, given_size):
        i = 0
        calc_size = given_size
        while True:
            if calc_size >= 1024:
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

    def select_size(self, givensize, choosenunit = 0):
        calc_size = givensize
        for i in range(choosenunit):
            calc_size = calc_size / 1024

        return calc_size

    def max_unit(self, givensize):
        i = 0
        calc_size = givensize
        while True:
            if calc_size >= 1024:
                calc_size = calc_size / 1024
                i = i + 1
            else:
                break
        return i

    def get_unit_name(self, i):
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

        return unit

    def get_date(self, time):
        dt = datetime.datetime.fromtimestamp(time)
        return "{0:02d}-{1:02d}-{2}".format(dt.day, dt.month, dt.year)

    def get_timedate(self, time):
        dt = datetime.datetime.fromtimestamp(time)
        return "{0}-{1:02d}-{2:02d} {3:02d}-{4:02d}-{5:02d}".format(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
        )

