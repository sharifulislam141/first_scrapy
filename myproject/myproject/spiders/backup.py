import scrapy
from ..items import MyprojectItem


class MyfirstScrp(scrapy.Spider):
    name = 'quotes'
    page_number=2
    start_urls = [
        'https://quotes.toscrape.com/'
    ]

    def parse(self, response):
        items = MyprojectItem()
        all_div_quotes = response.css('div.quote')
        for quote in all_div_quotes:
            discription = quote.css('span.text::text').get()
            author = quote.css('.author::text').get()
            tags = quote.css('.tag::text').getall()
            items['discription'] = discription
            items['author'] = author
            items['tags'] = tags
            yield items

        next_page = 'https://quotes.toscrape.com/page/'+str(MyfirstScrp.page_number)+'/'
        if MyfirstScrp.page_number < 11 :
            MyfirstScrp.page_number += 1
            yield response.follow(next_page, callback=self.parse)
