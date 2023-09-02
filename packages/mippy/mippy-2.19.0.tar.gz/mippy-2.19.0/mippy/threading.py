# from multiprocessing import Pool, cpu_count, freeze_support, Lock
from multiprocessing import Pool, freeze_support, Lock
import time
from contextlib import closing
import sys
from psutil import cpu_count, virtual_memory
from .misc import cprint


from threadpoolctl import ThreadpoolController, threadpool_limits

# Generate a threadpoolcontroller
controller = ThreadpoolController()

# Decorator to limit number of numpy blas threads when multhreading
@controller.wrap(limits=1, user_api='blas') 
def multithread(func,input,progressbar=None,threads=None,status=None):
        #~ freeze_support()
        if threads is None:
                # threads=int(cpu_count())+1
                # Modified 10/8/23 to prevent memory errors on machines with ++CPU cores and --RAM.
                minimum_memory_per_thread = 200  # specify this in MB
                reserved_memory = 400 # specify this in MB
                available_memory = (virtual_memory().available)//(1024*1024)
                # available_memory = 2056         # Just to test the calculation
                max_threads_mem = (available_memory-reserved_memory)//minimum_memory_per_thread
                cprint("INFO: Reserved memory - {} MB".format(reserved_memory))
                cprint("INFO: Min memory per thread - {} MB".format(minimum_memory_per_thread))
                cprint("INFO: Available memory - {} MB".format(available_memory))
                cprint("INFO: Logical CPU cores - {}".format(cpu_count()))
                if max_threads_mem == 0:
                        max_threads_mem = 1
                max_threads_cpu = int(cpu_count())+1
                if max_threads_mem<max_threads_cpu:
                        cprint("WARNING: Number of threads limited by available RAM")
                        # cprint("INFO: Potential {} MB RAM per thread".format(available_memory//max_threads_mem))
                        threads=max_threads_mem
                else:
                        # cprint("INFO: Threads limited by available CPU cores")
                        # cprint("INFO: Potential {} MB RAM per thread".format(available_memory//max_threads_cpu))
                        threads=max_threads_cpu
        pool = Pool(threads)
        cprint("INFO: Running on {} threads".format(threads))
        # result = pool.map_async(func,input,chunksize=1)
        chunksize=1
        result = pool.map_async(func,input,chunksize)
        while not result.ready():
                if not progressbar is None:
                        progress = (float(len(input))-float(result._number_left*chunksize))/float(len(input))*100.
                        #~ print "PROGRESS", progress
                        progressbar(progress,update=False)
                if not status is None:
                        jobnumber = len(input)-result._number_left*chunksize + 1
                        status('Reading file: '+'/'.join([str(jobnumber),str(len(input))]))
                #~ print("num left: {}".format(result._number_left))
                # time.sleep(0.1)
        if not progressbar is None:
                progressbar(0.)
        if not status is None:
                status('')
        # print("Closing multiprocessing pool")
        pool.close()
        # print("Joining pool")
        pool.join()
        # print("Fetching pool results")
        return result.get()
