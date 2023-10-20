from typing import Iterable
from scrapy.http import Request

import scrapy, logging
# import pdb

# Настройка логгирования
logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# scrapy crawl quotes

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]
    url_begins_with = 'https://quotes.toscrape.com'
    login_url = 'https://quotes.toscrape.com/login'

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'quotes.json'
    }

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.FormRequest(self.login_url, formdata={'username': 'admin', 'password': 'admin'}, callback=self.after_login)

    def after_login(self, response) -> None:
        goodreads_urls = response.css('div.quote span a[href^="http://"]::attr(href)').get()
        logging.info(f'IF LOGIN SUCCESSFUL: {goodreads_urls}')

        next = response.css('nav li.next a::attr(href)').get()
        logging.info(f'[!!!] I have tried to find next button, this is what I Have: {next}')

        if next:
            logging.info(f'NEXT: {next}')
            self.next_url = self.url_begins_with + next
            logging.info(f'NEXT URL: {self.next_url}')
            # urls_to_parse.append(next_url)
            logging.info(f'GOING RECURSIVELY TO THE NEXT PAGE: {self.next_url}')
            yield scrapy.Request(url=self.next_url, callback=self.after_login)

        logging.info(f'TRYING TO FINALLY PARSE CURRENT PAGE.')
        yield from self.parse(response)  # вызываем parse с текущей страницы

    def parse(self, response):
        logging.info('INITIATE PARSING FOR QUOTES')
        items = response.css('div.quote')
        for item in items:
            quote = item.css('span.text::text').get()
            author = item.css('small.author::text').get()
            tags = item.css('a.tag::text').getall()
            # logging.info(f'FOUND: {author}, {tags}, {quote}')
            # pdb.set_trace()
            yield {
                'tags': tags,
                'author': author,
                'quote': quote
                }

