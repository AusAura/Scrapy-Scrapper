import scrapy
# import pdb

# scrapy crawl authors

class AuthorsSpider(scrapy.Spider):
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]
    url_begins_with = 'https://quotes.toscrape.com'
    
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'authors.json'
    }

    def parse(self, response):
  
        authors = response.css('div.quote span a::attr(href)').getall()
        print(f'GETTING URLS: {authors}')
        # pdb.set_trace()

        if authors:
            for author in authors:
                url = self.url_begins_with + author
                print(f'CRAWLING URL: {author, url}')
                # pdb.set_trace()
                yield scrapy.Request(url=url, callback=self.parse)

        else:
            fullname = response.css('h3.author-title::text').get()
            born_date = response.css('p span.author-born-date::text').get()
            born_location = response.css('p span.author-born-location::text').get()
            description = response.css('div.author-description::text').get()
            print(f'CRAWLING URL: {fullname, born_date, born_location, description}')
            # pdb.set_trace()
            yield {'fullname': fullname,
                   'born_date': born_date,
                   'born_location': born_location,
                   'description': description.strip()
            }

