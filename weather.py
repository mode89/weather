from datetime import date, timedelta
import data

START_DATE = date(1973, 3, 1)
END_DATE = date(1974, 9, 30)

INPUT_PARAMETERS = [
    "temp",
    "slp",
    "vis",
    "wind",
    "wind_max",
    "temp_max",
    "temp_min",
    "fog",
    "rain"
]

def daterange(start, end):
    for n in range((end - start).days):
        yield start + timedelta(n)

if __name__ == "__main__" :
    print("Loading data...")
    stations = data.load("data.txt")
    print("{0} stations".format(len(stations)))

    print("Checking data...")
    fmissdays = open("missdays.txt", "w")
    missdays_cnt = 0
    for day in daterange(START_DATE, END_DATE):
        for s in stations:
            if day not in stations[s]:
                fmissdays.write("{0} {1}\n".format(s, day))
                missdays_cnt += 1
    fmissdays.close()
    print("{0} missing records".format(missdays_cnt))
