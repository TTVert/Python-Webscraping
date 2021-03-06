# json_thread.py
# Lowes
# Created by Noah Christiano on 7/21/2014.
# noahchristiano@rochester.edu

from Queue import Queue
import threading
from lowes_json import LowesJson
from multiprocessing import Process

job_q = Queue()
result_q = Queue()

class ThreadUrl(): #threading.Thread
	thread_num = -1
	def __init__(self, i):
		#threading.Thread.__init__(self)
		self.thread_num = i

	def run(self):
		while True:
			collector = LowesJson()
			num = job_q.get()
			print 'Process ' + str(self.thread_num) + ' getting place: ' + "%05d" % num
			s = collector.get_stores(num)
			if s != None:
				result_q.put(s)
			job_q.task_done()

class ThreadQ(): #threading.Thread
	def file_contains(self, num):
		file = open('test.txt')
		duplicate = False
		for line in file:
			if line == num + '\n':
				print 'Found duplicate: ' + num
				duplicate = True
		file.close()
		return duplicate
	
	def write(self, results):
		for r in results:
			if not self.file_contains(r):
				file = open('test.txt', 'a')
				print 'Writing store: ' + r
				file.write(r + '\n')
				file.close()

	def writer(self):
		while True:
			if not result_q.empty():
				s = result_q.get()
				if s != None:
					write(s)
"""
t = ThreadQ(result_q)
t.daemon = True
t.start()
print 'Started Queue Thread'

for i in range(500, 100000):
	queue.put(i)

for i in range(1000):
	t = ThreadUrl(queue, i)
	#t.daemon = True
	t.start()
	print 'Started thread: ' + "%05d" % i + ' Total Threads: ' + str(threading.active_count())

queue.join()
"""

if __name__ == '__main__':
	for i in range(500, 100000):
		job_q.put(i)
	
	emptier = ThreadQ()
	e = Process(target=emptier.writer)
	e.start()
	print 'Started Queue Process'

	for i in range(7):
		getter = ThreadUrl(i)
		p = Process(target=getter.run)
		p.start()
		print 'Started process: ' + "%05d" % i
	
