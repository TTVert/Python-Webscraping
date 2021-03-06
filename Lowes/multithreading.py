# multithreading.py
# Lowes
# Created by Noah Christiano on 7/21/2014.
# noahchristiano@rochester.edu

from multiprocessing import Process, Queue, Pool
from lowes_automator import LowesAutomator
from database_builder import DatabaseBuilder
import sys
sys.path.append('~/Lowes/locations')
from collector import LocationsCollector

collector = LowesAutomator()
database = DatabaseBuilder()
products = [] #list of pickled lists of items from each store

#get list of store numbers
def get_stores():
	stores = []
	collector = LocationsCollector()
	locations  = collector.get_locations()
	for l in locations:
		if l.country != 'Canada':
			stores.append(l)
	return stores

def worker(store):
	return collector.get_products(store)

stores = get_stores()
if __name__ == '__main__':
	pool = Pool()
	for s in stores:
		print s.town + ', ' + s.state
	print len(stores)
	for s in stores:#[:3]
		products.append(pool.apply_async(worker, [s]))

database.initialize()
for p in products:
	try:
		for x in p.get():
			database.add(x)
	except:
		print 'Database write error'
