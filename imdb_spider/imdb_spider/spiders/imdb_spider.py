import scrapy
import pandas as pd
from ..items import ImdbSpiderItem
import time
import re


def get_movies(path):
    data = pd.read_csv(path)
    url = data['url']

    return url


class ImdbSpider(scrapy.Spider):
    start = time.clock()
    name = 'movies'
    allowed_domains = ['imdb.com']

    def start_requests(self):
        data = get_movies('/Users/konglingtong/PycharmProjects/machine_learning/FP/data/url.csv')
        urls = []
        for link in data:
            u = re.findall(r'https://www\.imdb\.com/title/tt\d+/', str(link))
            if len(u) is not 0:
                urls.append(u)
        for i in range(len(urls)):
            url = urls[i][0]
            if (i % 100) == 0:
                time.sleep(5)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = []
        item = ImdbSpiderItem()
        movie_url = response.url

        item['year'] = response.xpath('//*[@id="titleYear"]/a/text()').extract()

        item['RatePeople'] = response.xpath(
            '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/a/span/text()').extract()

        directors = response.xpath(
            '//div[@id="title-overview-widget"]/div[2]/div[1]/div[2]/a/text()').extract()
        item['movie_url'] = movie_url
        if len(directors) is not 0:
            director = directors
        else:
            director = response.xpath(
                '//*[@id="title-overview-widget"]/div[2]/div[2]/div[1]/div[2]/a/text()').extract()

        stars = response.xpath(
            '//div[@id="title-overview-widget"]/div[2]/div[1]/div[4]/a/text()').extract()
        if len(stars) is not 0:
            star = stars
        elif len(response.xpath(
                '//*[@id="title-overview-widget"]/div[2]/div[2]/div[1]/div[4]/a/text()').extract()) is not 0:
            star = response.xpath(
                '//*[@id="title-overview-widget"]/div[2]/div[2]/div[1]/div[4]/a/text()').extract()
        elif len(response.xpath('//*[@id="title-overview-widget"]/div[2]/div[1]/div[3]/a/text()').extract()) is not 0:
            star = response.xpath('//*[@id="title-overview-widget"]/div[2]/div[1]/div[3]/a/text()').extract()
        elif len(response.xpath(
                '//*[@id="title-overview-widget"]/div[2]/div[2]/div[1]/div[3]/a/text()').extract()) is not 0:
            star = response.xpath(
                '//*[@id="title-overview-widget"]/div[2]/div[2]/div[1]/div[3]/a/text()').extract()
        elif len(response.xpath(
                '//*[@id="title-overview-widget"]/div[2]/div[2]/div[1]/div[2]/a/text()').extract()) is not 0:
            star = response.xpath(
                '//*[@id="title-overview-widget"]/div[2]/div[2]/div[1]/div[2]/a/text()').extract()

        # rate = response.xpath(
        #     '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/div/text()').extract_first()
        # if rate is not None:
        #     item['rate'] = rate
        # else:
        #     item['rate'] = response.xpath('///*[@id="titleStoryLine"]/div[5]/span[1]/text()').extract_first()

        movie = response.xpath(
            '//div[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/h1/text()').extract_first()
        if len(movie) is not 0:
            item['movie'] = movie
        else:
            item['movie'] = response.xpath(
                '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/h1/text()').extract_first()

        review = response.xpath(
            '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()') \
            .extract_first()
        item['review'] = review

        item['Production'] = response.css('a[href^="/company/"]::text').extract()

        rate = response.css('.subtext::text').extract()[0]
        if len(rate) is not 0:
            item['rate'] = rate
        else:
            item['rate'] = 'No rate'

        item['runTime'] = response.xpath(
            '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/div/time/text()').extract()

        genre = response.xpath('//*[@id="titleStoryLine"]/div[4]/a/text()').extract()
        if len(genre) is not 0:
            item['genre'] = genre
        elif len(response.xpath('//*[@id="titleStoryLine"]/div[3]/a//text()').extract()) is not 0:
            item['genre'] = response.xpath('//*[@id="titleStoryLine"]/div[3]/a/text()').extract()
        elif len(response.xpath('//*[@id="titleStoryLine"]/div[2]/a/text()').extract()) is not 0:
            item['genre'] = response.xpath('//*[@id="titleStoryLine"]/div[2]/a/text()').extract()
        elif len(response.xpath('//*[@id="titleStoryLine"]/div[1]/a/text()').extract() is not 0):
            item['genre'] = response.xpath('//*[@id="titleStoryLine"]/div[1]/a/text()').extract()

        country = response.css('.article a[href^="/search/title?country_of_origin="]::text').extract()
        item['country'] = country
        # if len(country) is not 0:
        #     item['country'] = country
        # elif len(response.xpath('//*[@id="titleDetails"]/div[2]/a/text()').extract()) is not 0:
        #     item['country'] = response.xpath('//*[@id="titleDetails"]/div[2]/a/text()').extract()

        item['cast'] = star + director

        if str(review) != 'nan':
            items.append(item)
            yield item

    # stop = time.clock()
    # print(stop - start)

    # for url in picture_urls:
    #     yield scrapy.Request(url=url, callback=self.picture_parse)

    # @staticmethod
    # def picture_parse(response):
    #     items = []
    #     item = ImdbSpiderItem()
    #     item['poster'] = response.xpath('//*[@id="photo-container"]/div/div[2]/div/div[2]/div[1]/div[2]/div/img[2]')
    #     yield item
    #     pass
