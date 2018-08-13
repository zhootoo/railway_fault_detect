import subprocess
from threading import Thread,Lock
from time import time
from time import sleep
from queue import deque,Queue
def run_sleep(period):
    proc = subprocess.Popen(['ping','-n',str(period),'127.0.0.1'])
    return proc
def factorize(number):
    for i in range(1,number+1):
        if number % i ==0:
            yield i
class Factor(Thread):
    def __init__(self,number):
        super().__init__()
        self.number = number
    def run(self):
        self.factors = list(factorize(number))
class Counter:
    def __init__(self):
        self.lock = Lock()
        self.count  = 0
    def increment(self,offset):
        with self.lock:
            self.count +=offset
def worker(index,how_many,counter):
    for _ in range(how_many):
        counter.increment(1)
def run_threads(func,how_many,counter):
    threads = []
    for i in range(5):
        args = (i,how_many,counter)
        thread = Thread(target=func,args=args)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
class MyQueue:
    def __init__(self):
        self.items = deque()
        self.lock = Lock()

    def put(self,item):
        with self.lock:
            self.items.append(item)

    def get(self):
        with self.lock:
            return self.items.popleft()

class Worker(Thread):
    def __init__(self,func,in_queue,out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.poll_count = 0
        self.work_done = 0
    def run(self):
        while True:
            self.poll_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
                sleep(0.01)
            else:
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done += 1
class ClosableQueue(Queue):
    SENTINEL = object()
    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return
                yield item
            finally:
                self.task_done()

class StopableWork(Thread):
    def __init__(self,func,in_queue,out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)




def download(item):
    return item
def resize(item):
    return item
def upload(item):
    return item
if __name__=='__main__':
    # how_many = 10**5
    # counter = Counter()
    # run_threads(worker,how_many,counter)
    # print(counter.count)
    # download_queue = MyQueue()
    # resize_queue = MyQueue()
    # upload_queue = MyQueue()
    # done_queue = MyQueue()
    # threads = [Worker(download,download_queue,resize_queue),
    #            Worker(resize,resize_queue,upload_queue),
    #            Worker(upload,upload_queue,done_queue)]
    # for thread in threads:
    #     thread.start()
    # for _ in range(1000):
    #     download_queue.put(object())
    # while len(done_queue.items)<1000:
    #     pass
    # processed = len(done_queue.items)
    # polled = sum(t.poll_count for t in threads)
    # print(polled)
    download_queue = ClosableQueue()
    resize_queue = ClosableQueue()
    upload_queue = ClosableQueue()
    done_queue = ClosableQueue()
    threads = [StopableWork(download,download_queue,resize_queue),
              StopableWork(resize,resize_queue,upload_queue),
              StopableWork(upload,upload_queue,done_queue) ]
    for thread in threads:
        thread.start()
    for _ in range(1000):
        download_queue.put(object())
    download_queue.close()
    download_queue.join()
    resize_queue.close()
    resize_queue.join()
    upload_queue.close()
    upload_queue.join()
    print(done_queue.qsize())
