# -*- coding: utf-8 -*-
import scrapy
from ..items import BoxofficeItem
import re


class ExampleSpider(scrapy.Spider):
    name = 'box'
    allowed_domains = ['boxofficemojo.com']

    def start_requests(self):
        for n in range(23):
            num = 1995 + n
            url = 'https://www.boxofficemojo.com/yearly/chart/?yr=%d&amp;p=.htm' % num
            yield scrapy.Request(url=url, callback=self.first_parse)

    def first_parse(self, response):
        urls = [response.url]
        url_pages = response.css('center font[face="Verdana"] a::attr(href)').extract()
        for s in url_pages:
            if s not in urls:
                u = 'https://www.boxofficemojo.com/' + s
                urls.append(u)
            # url = 'https://www.boxofficemojo.com/yearly/chart/?yr=2017&p=.htm' % (i + 1) +
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # item = BoxofficeItem()
        urls = response.css('tr td font a::attr(href)').extract()
        match = re.compile(r'[/][movies]+[/?id=\d\w.htm]+')
        movie_urls = []
        ls = []
        for url in urls:
            movie_url = match.findall(url)
            ls += movie_url
        for i in ls:
            if len(i) is not 0:
                movie_urls.append('https://www.boxofficemojo.com' + i)

        # yield item
        for url in movie_urls:
            yield scrapy.Request(url=url, callback=self.second_parse)

    @staticmethod
    def second_parse(response):
        items = []
        item = BoxofficeItem()
        item['box_office'] = response.css('tr td[width="35%"] b::text').extract()[0]
        ls = response.css('font[face="Verdana"] b::text').extract()
        ls.pop(0)
        item['movie'] = ls
        item['year'] = response.css('td[valign="top"] b a::text').extract()[1]
        item['distributor'] = response.css('td[valign="top"] b a::text').extract()[0]
        items.append(item)
        yield item
