
import multiprocessing
import queue
import json
import sys
import requests
import os
import argparse
import csv
import glob
import multiprocessing
import os
import pandas as pd
import queue
import requests
import sys
import time
import json
import operator

from html.parser import HTMLParser
from lxml import html
from multiprocessing import Queue


# Useful for debugging concurrency issues.
def log(msg):
    print(sys.stderr, multiprocessing.current_process().name, msg)


# Each worker reads the json file, computes a sum and a count for the target
# field, then stores both in the output queue.
def task(in_q, out_q):

    dictt = {}

    try:
        while (True):
            f = in_q.get(block=False)
            with open(f) as json_file:
                # print(json.loads(json_file))
                for line in json_file:
                    data = json.loads(line)
                    stop_and_search = data['stop-and-search']
                    for street in stop_and_search:
                        if street not in dictt.keys():
                            dictt[street] =1
                        else:
                            dictt[street] += 1
        print(dictt)
    except queue.Empty:
        pass  #print "Done processing"

    out_q.put(dictt)


def main_task(cnt):
    nprocs = int(cnt)


    url = "https://data.police.uk/api/crimes-street-dates"
    response = requests.get(url, timeout=1)
    http_status = response.status_code
    if (http_status != 200):
        print('ERROR: request failed with HTTP status code ', http_status)
        return

    readfrom = json.loads(response.content)

    q = multiprocessing.Queue()
    out_q = multiprocessing.Queue()

    out_filename = "crime_data/"
    os.makedirs(os.path.dirname(out_filename), exist_ok=True)

    for i in range(len(readfrom)):
        tmp = readfrom[i]
        tmp_name = "crime_data/%d.json" % (i)
        with open(tmp_name, 'w') as outfile:
            json.dump(tmp, outfile)
        q.put(tmp_name)




    procs = []
    for i in range(nprocs):
        p = multiprocessing.Process(target=task, args=(q, out_q))
        p.start()
        procs.append(p)

    # Main task takes partial results and computes the final average.
    dictt = {}

    for p in procs:
        p_dict = out_q.get()
        if not bool(dictt):
            dictt = p_dict
        else: 
            for k in (set(dictt) | set(p_dict)):
                dictt[k] = dictt.get(k, 0) + p_dict.get(k, 0)

    # print('average = %.2f' % (sum / cnt))
    print("stats on each street")
    print(dictt)
    worst_street = max(dictt.items(), key=operator.itemgetter(1))[0]
    print("the worst street is %s with %d many stop-and-searches" % (worst_street, dictt[worst_street]))

# python3 queue_test.py <n_cores>
if __name__ == "__main__":
    main_task(sys.argv[1])



























