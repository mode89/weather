import data

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

if __name__ == "__main__" :
    stations = data.load("data.txt")
