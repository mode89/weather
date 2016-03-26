from datetime import date, timedelta
import data

START_DATE = date(1973, 3, 1)
END_DATE = date(1974, 9, 30)

PARAMETERS = [
    "temp",
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
    fmissvals = open("missvals.txt", "w")
    missvals_cnt = 0
    for day in daterange(START_DATE, END_DATE):
        for s in stations:
            if day not in stations[s]:
                fmissdays.write("{0} {1}\n".format(s, day))
                missdays_cnt += 1
            else:
                record = stations[s][day]
                for p in PARAMETERS:
                    if getattr(record, p) is None:
                        fmissvals.write("{0} {1} {2}\n".format(s, day, p))
                        missvals_cnt += 1
    fmissdays.close()
    fmissvals.close()
    print("{0} missing records".format(missdays_cnt))
    print("{0} missing values".format(missvals_cnt))
    print("{0} parameters".format(len(PARAMETERS)))

    print("Calibrating...")
    input_cnt = len(PARAMETERS) * len(stations)
    min_values = [float("inf")] * input_cnt
    max_values = [float("-inf")] * input_cnt
    for day in daterange(START_DATE, END_DATE):
        values = list()
        for s in stations:
            record = stations[s][day]
            for p in PARAMETERS:
                values.append(getattr(record, p))
        for i in range(input_cnt):
            if values[i] is not None:
                min_values[i] = min(float(values[i]), min_values[i])
                max_values[i] = max(float(values[i]), max_values[i])
    input_scaling = [1.0 / (max_values[i] - min_values[i])
        for i in range(input_cnt)]
    input_bias = [-0.5 * (max_values[i] - min_values[i])
        for i in range(input_cnt)]
