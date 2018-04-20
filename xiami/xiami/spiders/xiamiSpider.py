# -*- coding: utf-8 -*-
import scrapy
from xiami.items import XiamiItem
import win_unicode_console
from scrapy_redis.spiders import RedisCrawlSpider

win_unicode_console.enable()


class xiamiSpider(RedisCrawlSpider):
    name = 'xiami'
    allowed_domains = ['xiami.com']
    redis_key = "xiamiSpider:start_urls"

    def start_requests(self):
        urls = ['http://www.xiami.com/collect/recommend/page/%s' % (str(x+1)) for x in range(50)]
        return [scrapy.Request(url,callback=self.parse) for url in urls ]
        # for url in urls :
        #     yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):

        id_list = response.xpath('//p[@class="collect_info"]')

        for id in id_list:
            href = id.xpath('.//span/a/@href').extract_first()
            # print('http://www.xiami.com' + href)
            yield scrapy.Request('http://www.xiami.com/space/charts-recent' + href + '/page/1'
                                 , callback=self.parse_user, meta={'href': href})

    def parse_user(self, response):
        ## 最多抓取一千条
        href = response.meta['href']
        item = XiamiItem()
        song_list = response.xpath('//td[@class="song_name"]')
        for song in song_list:
            res = song.xpath('.//a/text()').extract()
            item['userid'] = href.split(r'/')[-1]
            if (len(res) != 0):
                item['name'] = res[0] + '-' + res[1]
                yield item
        next_list = response.xpath('//a[@class="p_redirect_l"]/@href').extract()
        if (len(next_list) != 0):
            yield scrapy.Request('http://www.xiami.com' + next_list[0], callback=self.parse_user, meta={'href': href})
