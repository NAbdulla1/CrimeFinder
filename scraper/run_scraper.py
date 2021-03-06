from scraper.scraper.spiders.kalerkantho import Kalerkantho
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os


class Scraper:
    def __init__(self):
        settings_file_path = 'scraper.scraper.settings'  # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerProcess(get_project_settings())
        self.spider = Kalerkantho  # The spider you want to crawl

    def run_spiders(self):
        self.process.crawl(self.spider)
        self.process.start()
