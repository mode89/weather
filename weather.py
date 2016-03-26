from datetime import date, timedelta
import data
import esn

START_DATE = date(1973, 3, 1)
END_DATE = date(1998, 9, 30)
NEURONS_COUNT = 512
CONNECTIVITY = 0.5
WASHOUT_COUNT = 20
WASHOUT_START = START_DATE
WASHOUT_END = WASHOUT_START + timedelta(WASHOUT_COUNT)

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

def make_param_list(day):
    inputs = list()
    for s in STATIONS:
        if day in STATIONS[s]:
            record = STATIONS[s][day]
            for p in PARAMETERS:
                value = getattr(record, p)
                inputs.append(float(value)
                    if value is not None else None)
        else:
            for p in PARAMETERS:
                inputs.append(None)
    return inputs

if __name__ == "__main__" :
    print("Loading data...")
    STATIONS = data.load("data.txt")
    print("{0} stations".format(len(STATIONS)))
    for s in STATIONS:
        print(s)

    print("Checking data...")
    fmissdays = open("missdays.txt", "w")
    missdays_cnt = 0
    fmissvals = open("missvals.txt", "w")
    missvals_cnt = 0
    for day in daterange(START_DATE, END_DATE):
        for s in STATIONS:
            if day not in STATIONS[s]:
                fmissdays.write("{0} {1}\n".format(s, day))
                missdays_cnt += 1
            else:
                record = STATIONS[s][day]
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
    input_cnt = len(PARAMETERS) * len(STATIONS)
    min_values = [float("inf")] * input_cnt
    max_values = [float("-inf")] * input_cnt
    for day in daterange(START_DATE, END_DATE):
        values = make_param_list(day)
        for i in range(input_cnt):
            if values[i] is not None:
                min_values[i] = min(float(values[i]), min_values[i])
                max_values[i] = max(float(values[i]), max_values[i])
    input_scaling = [1.0 / (max_values[i] - min_values[i]) * 0.01
        for i in range(input_cnt)]
    input_bias = [-0.5 * (max_values[i] - min_values[i])
        for i in range(input_cnt)]
    output_scale = [max_values[i] - min_values[i]
        for i in range(input_cnt)]
    output_bias = [(max_values[i] + min_values[i]) / 2.0
        for i in range(input_cnt)]

    print("Constructing network...")
    network = esn.Network(
        ins=input_cnt,
        neurons=NEURONS_COUNT,
        outs=input_cnt,
        has_ofb=False,
        cnctvty=CONNECTIVITY)
    network.set_input_scalings(input_scaling)
    network.set_input_bias(input_bias)
    network.set_output_scale(output_scale)
    network.set_output_bias(output_bias)

    print("Washing out...")
    for day in daterange(WASHOUT_START, WASHOUT_END):
        inputs = make_param_list(day)
        for i in range(input_cnt):
            if inputs[i] is None:
                inputs[i] = 0.0
        network.set_inputs(inputs)
        network.step(1.0)

    print("Washing out untrainable days...")
    for day in daterange(WASHOUT_END, END_DATE):
        inputs = make_param_list(day)
        if None not in inputs:
            WASHOUT_END = day
            break
        else:
            for i in range(input_cnt):
                if inputs[i] is None:
                    inputs[i] = 0.0
            network.set_inputs(inputs)
            network.step(1.0)

    print("Training...")
    for day in daterange(WASHOUT_END, END_DATE):
        print(day)
        inputs = make_param_list(day)
        for i in range(input_cnt):
            if inputs[i] is None:
                inputs[i] = outputs[i]
        network.set_inputs(inputs)
        network.step(1.0)
        outputs = network.capture_output(input_cnt)
        ref_outputs = make_param_list(day + timedelta(1))
        if None not in ref_outputs:
            print("{0} {1}".format(outputs[0], ref_outputs[0]))
            network.train_online(ref_outputs, forceOutput=False)
        else:
            print("Trainining skipped.")
        for i in range(input_cnt):
            if ref_outputs[i] is not None:
                outputs[i] = ref_outputs[i]
