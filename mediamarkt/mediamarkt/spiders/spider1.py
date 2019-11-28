import scrapy
import re

filename = 'tv_prices.txt'
base_url = "https://mediamarkt.se"


class IntroSpider(scrapy.Spider):
    name = "intro_spider"

    ## The first request to perform is defined in the start_requests method
    # This is what is called when the Spider is first executed
    # Here we define the list of URLs for which to make requests
    # We also specify the callback function to do the actual parsing
    def start_requests(self):

        # We scrape the first 5 pages of books to scrape
        urls = [
                'https://www.mediamarkt.se/sv/category/_alla-tv-apparater-564040.html? \
                view=PRODUCTLIST&page=1&sort=topseller'
        ]

        # We generate a Request for each URL
        # We also specify the use of the parse function to parse the responses
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # Define how to handle the response object in the parse function
    # Here, we extract the book titles and write it to a file
    def parse(self, response):

        # Extract the list of book titles into a list
        tv_list = response.xpath('//*[@id="category"]/ul/li/script/text()').extract()
        prices = []

        for tv in tv_list:
            m = re.search('{(.+?)}', tv)
            split_text = m.group(1).split(',')
            for n in split_text:
                if "price" in n:
                    split_price = n.split(':')
                    prices.append(split_price[1].strip('\"'))

        with open(filename, 'a+') as f:
            for price in prices:
                f.write(price + "\n")

        next_pages = response.xpath('//*[@id="category"]/div[2]/ul/li/a/@href').extract()
        page_number = 2
        if next_pages:
            for next_page in next_pages:
                if "page="+str(page_number) in next_page:
                    url = base_url + next_page
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse
                        )
                    page_number += 1

