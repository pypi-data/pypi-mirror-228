# -*- coding: utf-8 -*-

import orjson


def open_file(file):
    print()
    try:
        print("open", file, "...")

        json_data = None

        with open(file, "r") as f:
            json_data = orjson.loads(f.read())

        return json_data
    except Exception as e:
        print("open_file Exception:", e)


def save_file(file_name, data):
    try:
        with open(file_name, "wb") as f:
            f.write(orjson.dumps(data))

        print("Yep", file_name, "succesfully generated.")
    except Exception as e:
        print("save_file: Oops, definitely can not generate file...", e)
