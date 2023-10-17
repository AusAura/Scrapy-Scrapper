from scrapy.crawler import CrawlerProcess
from quotes_spyder.quotes_spyder.spiders.quotes import QuotesSpider 
from quotes_spyder.quotes_spyder.spiders.authors import AuthorsSpider


process_au = CrawlerProcess(settings={
    'FEEDS': {
        'authors.json': {
            'format': 'json',
            'encoding': 'utf8',
            'store_empty': False,
            'fields': None,
            'indent': 4
        }
    }
})
process_qu = CrawlerProcess(settings={
    'FEEDS': {
        'quotes.json': {
            'format': 'json',
            'encoding': 'utf8',
            'store_empty': False,
            'fields': None,
            'indent': 4,
            'item_export_kwargs': {
                'ensure_ascii': False
            },
        }
    }
})
process_qu.crawl(QuotesSpider)
process_au.crawl(AuthorsSpider)
process_au.start()
process_qu.start()