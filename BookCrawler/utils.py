import os, time, json, sys
import urllib3
import pandas as pd
from datetime import datetime
DEFAULT_TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"


def get_time_str(time=datetime.now(), fmt=DEFAULT_TIME_FORMAT):
    try:
        return time.strftime(fmt)
    except:
        return ""


def get_time_obj(time_str, fmt=DEFAULT_TIME_FORMAT):
    try:
        return datetime.strptime(time_str, fmt)
    except:
        return None


def transform_time_fmt(time_str, src_fmt, dst_fmt=DEFAULT_TIME_FORMAT):
    time_obj = get_time_obj(time_str, src_fmt)
    time_str = get_time_str(time_obj, dst_fmt)
    return time_str


def mkdirs(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def load_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def save_json(data, path):
    dir = path[:path.rfind("/")]
    mkdirs(dir)

    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False)
    print("Save json data (size = {}) to {} done".format(len(data), path))


def save_csv(df, path, fields=None):
    dir = path[:path.rfind("/")]
    mkdirs(dir)
    if fields is None or len(fields) == 0:
        columns = df.columns
    else:
        columns = fields
    df.to_csv(path, index=False, columns=columns)
    print("Save csv data (size = {}) to {} done".format(df.shape[0], path))


def load_list(path):
    data = []
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = f.readlines()
        data = [e.strip() for e in data]

    return data


def save_list(data, path):
    dir = path[:path.rfind("/")]
    mkdirs(dir)

    with open(path, 'w') as f:
        f.write("\n".join(data))
    print("Save list data (size = {}) to {} done".format(len(data), path))


def save_str(str, path):
    dir = path[:path.rfind("/")]
    mkdirs(dir)

    with open(path, 'w') as f:
        f.write(str)
    print("Save string to {} done".format(path))
