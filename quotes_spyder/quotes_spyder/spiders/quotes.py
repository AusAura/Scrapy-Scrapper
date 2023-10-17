import scrapy
# import pdb


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'quotes.json'
    }

    def parse(self, response):
        items = response.css('div.quote')
        for item in items:
            quote = item.css('span.text::text').get()
            author = item.css('small.author::text').get()
            tags = item.css('a.tag::text').getall()
            # print(author, tags, quote)
            # pdb.set_trace()
            yield {
                'tags': tags,
                'author': author,
                'quote': quote
                }

