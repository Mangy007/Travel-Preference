# -*- coding: utf-8 -*-
import scrapy
import pandas as pd


class MouthshutTravelReviewsSpider(scrapy.Spider):
    name = 'mouthshut_travel_reviews'
    allowed_domains = ['mouthshut.com']
    start_urls = ['https://www.mouthshut.com/product/categories.php?cid=142/']

    def parse(self, response):
        # listings = response.css('.rtitle')
        place_list = response.xpath(
            '//div[@id="categorierightpanel"]//div//div[@class="categories categoriesscroll"]//div[@class="rtitle"]//a')
        places = []
        places_link = []
        for place in place_list:
            place_name = place.xpath("text()").get().strip()
            place_review_link = response.urljoin(place.xpath(
                '@href').get().strip())
            places.append(place_name)
            places_link.append(place_review_link)
            yield scrapy.Request(
                place_review_link, callback=self.parse_place_review_page, meta={"place": place_name})
        pass

    def parse_place_review_page(self, response):
        review_list = response.xpath(
            '//div[@id="dvreview-listing"]//div[@class="row review-article"]//div[@class="col-10 review"]')
        reviews = []
        for review in review_list:
            review_params = review.css(
                'div.reviewdata a::attr(onclick)').get().strip()
            review_link = review_params.split(',')[-4].replace("'", '')
            request = scrapy.Request(
                review_link, callback=self.parse_review_page, meta={"place": response.meta.get("place")})
            yield request
        pass

    def parse_review_page(self, response):
        review_list = response.xpath(
            '//div[@class="rev-main-content"]//p')
        review = ""
        for rev in review_list:
            review += " "+rev.xpath('text()').get().strip()
        return {"review": review.strip(), "place": response.meta.get("place")}
