#diff
import multiprocessing
import queue
import json
import sys
import time
from time import perf_counter

#parallel filter, implemented on column: status, and value: success.


# Useful for debugging concurrency issues.
def log(msg):
    print(sys.stderr, multiprocessing.current_process().name, msg)


# Each worker reads the json file, computes a sum and a count for the target
# field, then stores both in the output queue.
def task(in_q, out_q):
    filtered = []

    try:
        while (True):
            f = in_q.get(block=False)
            with open(f) as json_file:
                for line in json_file:
                    data = json.loads(line)
                    if data["status"] == "success":
                        filtered.append(data)

    except queue.Empty:
        pass  #print "Done processing"

    out_q.put(filtered)


def main_task(cnt):
    nprocs = int(cnt)

    q = multiprocessing.Queue()
    out_q = multiprocessing.Queue()

    # Enqueue filenames to be processed in parallel.
    for i in range(100):
        f = "data/json/mybinder%03d.json" % (i)
        q.put(f)

    procs = []
    start_time = time.perf_counter()
    for i in range(nprocs):
        p = multiprocessing.Process(target=task, args=(q, out_q))
        p.start()
        procs.append(p)

    # Main task takes partial results and computes the final average.
    all_filtered = []

    for p in procs:
        p_filtered = out_q.get()
        all_filtered = all_filtered + p_filtered

    end_time = time.perf_counter()    
    print("Num Workers: %s, Time: %d" % ( cnt, (end_time-start_time)*1000) )

    print('num succeess = %d' % (len(all_filtered)))


# python3 queue_test.py <n_cores>
if __name__ == "__main__":
    main_task(sys.argv[1])
