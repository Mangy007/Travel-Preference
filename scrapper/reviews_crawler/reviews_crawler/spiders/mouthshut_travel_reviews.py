# -*- coding: utf-8 -*-
import scrapy
import pandas as pd


class MouthshutTravelReviewsSpider(scrapy.Spider):
    name = 'mouthshut_travel_reviews'
    allowed_domains = ['mouthshut.com']
    start_urls = ['https://www.mouthshut.com/product/categories.php?cid=142/']

    def parse(self, response):
        # listings = response.css('.rtitle')
        listings = response.xpath('//div[@id="categorierightpanel"]//div//div[@class="categories categoriesscroll"]//div[@class="rtitle"]//a')
        places = []
        places_link = []
        print('aaya')
        print(len(listings))
        for place in listings:
            print('-----------')
            place_name = place.xpath("text()").get().strip()
            place_review_link = place.xpath('@href').get().strip()
            places.append(place_name)
            places_link.append(place_review_link)
            request = response.follow(place_review_link, callback=self.parse)
            break
        pass
