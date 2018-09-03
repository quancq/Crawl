import os, time, json
from datetime import datetime, timedelta
import pandas as pd

DEFAULT_TIME_FORMAT = "%Y-%m-%d"
DEFAULT_DELIMITER = " - "


def mkdirs(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def get_time_str(time=datetime.now(), fmt=DEFAULT_TIME_FORMAT):
    return time.strftime(fmt)


def get_time_obj(time_str, fmt=DEFAULT_TIME_FORMAT):
    return datetime.strptime(time_str, fmt)


def save_json(data, path):
    dir = path[:path.rfind("/")]
    mkdirs(dir)

    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)
    print("Save json data (size = {}) to {} done".format(len(data), path))


def load_json(path):
    data = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)

    return data


def generate_datetime_objs(start_date, end_date):
    duration_day = (end_date - start_date).days

    if duration_day > 0:
        step = 1
    elif duration_day < 0:
        step = -1
    duration_day += step
    for duration in range(0, duration_day, step):
        yield start_date + timedelta(days=duration)


def get_specific_fmt_time(date):
    return str(date.day), str(date.month), str(date.year)


if __name__ == "__main__":
    start_date = datetime(year=2018, month=3, day=4)
    end_date = datetime(year=2018, month=2, day=4)

    days = [get_time_str(day) for day in generate_datetime_objs(start_date, end_date)]
    print('\n'.join(days))
