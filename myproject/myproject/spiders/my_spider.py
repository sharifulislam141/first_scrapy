import scrapy
from scrapy.http import FormRequest
from ..items import MyprojectItem


class MyfirstScrp(scrapy.Spider):
    name = 'quotes'
    page_number = 2
    start_urls = [
        'https://quotes.toscrape.com/login'
    ]

    def parse(self, response):
        # Extract CSRF token value
        token = response.css('form input[name="csrf_token"]::attr(value)').extract_first()
        
        # Create form data for login
        return FormRequest.from_response(
            response,
            formdata={
                'csrf_token': token,
                'username': 'test',  # Replace with your username
                'password': 'test'   # Replace with your password
            },
            callback=self.start_scraping
        )

    def start_scraping(self, response):
        # Now you are logged in, scrape the quotes
        items = MyprojectItem()

        all_div_quotes = response.css('div.quote')

        for quote in all_div_quotes:
            discription = quote.css('span.text::text').extract_first()
            author = quote.css('small.author::text').extract_first()
            tags = quote.css('div.tags a.tag::text').extract()

            items['discription'] = discription
            items['author'] = author
            items['tags'] = tags

            yield items

        # Follow pagination link
        next_page = f'https://quotes.toscrape.com/page/{self.page_number}/'
        if self.page_number <= 10:
            self.page_number += 1
            yield response.follow(next_page, callback=self.start_scraping)
