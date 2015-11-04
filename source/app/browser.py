#!/usr/bin/python
import sys
import os
import json
from collections import OrderedDict
import datetime

TO_NICE_DISPLAY = {
    0: 'B',
    1: 'KB',
    2: 'MB',
    3: 'GB',
    4: 'TB'
}

ROOT_FOLDER = '/Users/bvallet/Desktop/sms_data'

def size_to_nice_display(size):
    """
    Display size with the correct unit
    Works only for stuff < 9999 TB
    see http://svn.lacie.com/svn/playground/blegrand/tests/nice_number_display.py
    for tests
    """
    from math import pow
    if -1 == size:
        return '-'
    division = 0
    result_size = size

    while ((len(TO_NICE_DISPLAY) - 1) > division) and (1024 <= result_size):
        division += 1
        result_size = size / (pow(1024, division))

    if 0 != division:
        # We want to keep at most 1 decimal
        result_size = int(result_size * 10)
        #We have to recast into float in order to keep the deciman
        result_size = float(result_size) / 10
    return "%s %s" % (result_size, TO_NICE_DISPLAY[division])

def browse(path, folder_only=False, files_only=False, recursive=True):
    path = os.path.join(ROOT_FOLDER, path[1:])

    if not os.path.isdir(path):
        print("Path: %s does not exist", path)
        return
    if path[-1] != "/":
        path = path + "/"

    result_dict = OrderedDict()

    if recursive:
        for root, dirs, files in os.walk(path):
            fakePath = root[len(path):]
            currentDictSplitted = fakePath.split("/")
            workOn = result_dict
            for key in currentDictSplitted:
                if 0 != len(key):
                    workOn = workOn[key]["subFolder"]
            if not files_only:
                for d in dirs:
                    if d.startswith("."):
                        continue
                    workOn[d] = {
                        "isDir": True,
                        "name": d,
                        "subFolder": OrderedDict(),
                        "size": "-",
                        "kind": "folder",
                        "mDate": datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(root, d))).strftime('%Y-%m-%d %H:%M:%S')
                    }
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            if not folder_only:
                for f in files:
                    workOn[f] = {
                        "isDir": False,
                        "name": f,
                        "url": os.path.join(fakePath, f),
                        "size": size_to_nice_display(os.path.getsize(os.path.join(root, f))),
                        "kind": os.path.splitext(os.path.join(root, f))[1][1:],
                        "mDate": datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(root, f))).strftime('%Y-%m-%d %H:%M:%S')
                    }
    else:
        for item in os.listdir(path):
            fakePath = path
            currentDictSplitted = fakePath.split("/")
            workOn = result_dict
            # for key in currentDictSplitted:
            #     if 0 != len(key):
            #         workOn = workOn[key]["subFolder"]

            if os.path.isdir(os.path.join(path, item)):
                if not files_only:
                    if item.startswith("."):
                        continue
                    workOn[item] = {
                        "isDir": True,
                        "name": item,
                        "subFolder": OrderedDict(),
                        "size": "-",
                        "kind": "folder",
                        "mDate": datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(path, item))).strftime('%Y-%m-%d %H:%M:%S')
                    }
            else:
                if not folder_only:
                    workOn[item] = {
                        "isDir": False,
                        "name": item,
                        "url": os.path.join(fakePath, item),
                        "size": size_to_nice_display(os.path.getsize(os.path.join(path, item))),
                        "kind": os.path.splitext(os.path.join(path, item))[1][1:],
                        "mDate": datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(path, item))).strftime('%Y-%m-%d %H:%M:%S')
                    }

    return json.dumps(result_dict)

if __name__ == "__main__":
    if 4 != len(sys.argv):
        print("usage: %s path_to_browse url_prefix outputFile" % sys.argv[0])
        sys.exit(1)
    path = sys.argv[1]

    if not os.path.isdir(path):
        print("Path: %s does not exist", path)
        sys.exit(2)
    if path[-1] != "/":
        path = path + "/"
    result_dict = OrderedDict()
    for root, dirs, files in os.walk(path):
        fakePath = root[len(path):]
        currentDictSplitted = fakePath.split("/")
        workOn = result_dict
        for key in currentDictSplitted:
            if 0 != len(key):
                workOn = workOn[key]["subFolder"]
        for d in dirs:
            if d.startswith("."):
                continue
            workOn[d] = {
                "isDir": True,
                "name": d,
                "subFolder": OrderedDict(),
                "size": "-",
                "kind": "folder",
                "mDate": datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(root, d))).strftime('%Y-%m-%d %H:%M:%S')
            }
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for f in files:
            workOn[f] = {
                "isDir": False,
                "name": f,
                "url": os.path.join(sys.argv[2], fakePath, f),
                "size": size_to_nice_display(os.path.getsize(os.path.join(root, f))),
                "kind": os.path.splitext(os.path.join(root, f))[1][1:],
                "mDate": datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(root, f))).strftime('%Y-%m-%d %H:%M:%S')
            }
    with open(sys.argv[3], "w") as f:
        json.dump(result_dict, f, indent=2)
