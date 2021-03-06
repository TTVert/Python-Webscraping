# collector.py
# Lowes
# Created by Noah Christiano on 7/21/2014.
# noahchristiano@rochester.edu

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from locations.spiders.allstays import AllstaysSpider
from scrapy.utils.project import get_project_settings
from store import Store

class LocationsCollector():
	
	items = []
	def add_item(self, item):
		self.items.append(item)

	def convertData(self, items):
		group = []
		for i in items:
			new = Store()
			new.set_state(i['state'])
			new.town = i['town']
			new.address = i['address']
			new.store_number = i['store_number']
			group.append(new)
		return group

	def get_locations(self):
		spider = AllstaysSpider(domain='allstays.com')
		settings = get_project_settings()
		crawler = Crawler(settings)
		crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
		crawler.signals.connect(self.add_item, signals.item_scraped)
		crawler.configure()
		crawler.crawl(spider)
		crawler.start()
		#log.start()
		reactor.run()
		return  self.convertData(self.items)
