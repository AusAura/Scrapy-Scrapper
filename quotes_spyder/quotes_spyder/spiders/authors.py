from typing import Iterable, Union
import scrapy
from scrapy.http import Request
import logging
# import pdb

# Настройка логгирования
logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# scrapy crawl authors

class AuthorsSpider(scrapy.Spider):
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]
    url_begins_with = 'https://quotes.toscrape.com'
    login_url = 'https://quotes.toscrape.com/login'
    
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'authors.json'
    }

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.FormRequest(self.login_url, formdata={'username': 'admin', 'password': 'admin'}, callback=self.after_login)

    def after_login(self, response: scrapy.http.Response) -> None:
        goodreads_urls = response.css('div.quote span a[href^="http://"]::attr(href)').get()
        logging.info(f'IF LOGIN SUCCESSFUL: {goodreads_urls}')

        next = response.css('nav li.next a::attr(href)').get()
        logging.info(f'[!!!] I have tried to find next button, this is what I Have: {next}')

        if next:
            logging.info(f'NEXT: {next}')
            self.next_url = self.url_begins_with + next
            logging.info(f'NEXT URL: {self.next_url}')
            logging.info(f'GOING RECURSIVELY TO THE NEXT PAGE: {self.next_url}')
            yield scrapy.Request(url=self.next_url, callback=self.after_login)

        logging.info(f'TRYING TO FINALLY PARSE CURRENT PAGE.')
        yield from self.parse(response)  # вызываем parse с текущей страницы


    def parse(self, response: scrapy.http.Response) -> Union[scrapy.http.Response, dict]:
        logging.info('INITIATE PARSING')
        authors = response.css('div.quote span a::attr(href)').getall()
        external_urls = response.css('div.quote span a[href^="http://"]::attr(href)').getall()
        external_urls = set(external_urls)
        logging.info(f'GETTING URLS: {authors}')
        # pdb.set_trace()

        if authors:
            logging.info(f'LIST PAGE, COLLECTING LINKS.')
            for author in authors:
                prep_author = author.split('-')
                surname = prep_author[len(prep_author)-1]
                logging.info(f'FOUND SURNAME: {surname}')
                for link in external_urls:
                    logging.info(f'CHECKING LINK: {link}')
                    if surname in link:
                        logging.info(f'POSITIVE FOR {link}!!!')
                        external_url = link
                        break

                logging.info(f'AUTHOR: {author}')
                logging.info(f'EXTERNAL: {external_url}')
                url = self.url_begins_with + author
                logging.info(f'CRAWLING URL: {author, url}')
                # pdb.set_trace()
                yield scrapy.Request(url=url, callback=self.parse, meta={'external': external_url})

        else:
            logging.info(f'AUTHOR PAGE, COLLECTING DATA. META = {response.meta.get("external")}')
            fullname = response.css('h3.author-title::text').get()
            born_date = response.css('p span.author-born-date::text').get()
            born_location = response.css('p span.author-born-location::text').get()
            description = response.css('div.author-description::text').get()
            logging.info(f'CRAWLING URL: {fullname, born_date, born_location, description, response.meta.get("external")}')
            # pdb.set_trace()
            yield {'fullname': fullname,
                   'born_date': born_date,
                   'born_location': born_location,
                   'description': description.strip(),
                   'goodreads_url': response.meta.get('external')
            }

