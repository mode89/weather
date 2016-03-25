import datetime

def celcius(fahr):
    return (fahr - 32) * 5 / 9

def milmerc(milbar):
    return milbar * 0.750062

def km(miles):
    return miles * 1.60934

def ms(knots):
    return knots * 0.5144444

class Record:

    def __init__(self, line):
        vals = line.split()

        # Station code
        self.stn = vals[0]

        # Date
        self.date = datetime.datetime.strptime(vals[2], "%Y%m%d").date()

        # Mean temperature
        if vals[3] <> "9999.9":
            self.temp = celcius(float(vals[3]))
        else:
            self.temp = None

        # Mean sea level pressure
        if vals[7] <> "9999.9":
            self.slp = milmerc(float(vals[7]))
        else:
            self.slp = None

        # Mean station pressure
        if vals[9] <> "9999.9":
            self.stp = milmerc(float(vals[9]))
        else:
            self.stp = None

        # Mean visibility
        if vals[11] <> "999.9":
            self.vis = km(float(vals[11]))
        else:
            self.vis = None

        # Mean wind speed
        if vals[13] <> "999.9":
            self.wind = ms(float(vals[13]))
        else:
            self.wind = None

        # Maximum sustained wind speed
        if vals[15] <> "999.9":
            self.wind_max = ms(float(vals[15]))
        else:
            self.wind_max = None

        # Maximum wind gust
        if vals[16] <> "999.9":
            self.wind_gust = ms(float(vals[16]))
        else:
            self.wind_gust = None

        # Maximum temperature
        if vals[17] <> "9999.9":
            self.temp_max = celcius(float(
                vals[17][:-1] if vals[17].endswith("*") else vals[17]))
        else:
            self.temp_max = None

        # Minimum temperature
        if vals[18] <> "9999.9":
            self.temp_min = celcius(float(
                vals[18][:-1] if vals[18].endswith("*") else vals[18]))
        else:
            self.temp_min = None

        # Flags
        self.fog = vals[21][0] == '1'
        self.rain = vals[21][1] == '1'
        self.show = vals[21][2] == '1'
        self.hail = vals[21][3] == '1'
        self.thunder = vals[21][4] == '1'
        self.tornado = vals[21][5] == '1'

def load(fname):
    f = open(fname, "r")

    # Skip table header
    f.readline()

    stations = dict()
    for line in f:
        r = Record(line)
        if r.stn not in stations:
            stations[r.stn] = dict()
        stations[r.stn][r.date] = r

    return stations
