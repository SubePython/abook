# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from copy import deepcopy
from abook.items import AbookItem
class DdSpider(scrapy.Spider):
    name = 'dd'
    allowed_domains = ['x23us.com']
    start_urls = ['http://x23us.com/']

    def parse(self, response):
        li_list = response.xpath("//div[@class='main m_menu']/ul/li")[2:-2]
        for li in li_list:
            item = AbookItem()
            item["category"] = li.xpath("./a/text()").extract_first()
            item["category_url"] = "https://www.x23us.com/" + li.xpath("./a/@href").extract_first()
            if item["category_url"] is not None:
                yield scrapy.Request(
                    item["category_url"],
                    callback=self.parse_url,
                    meta={"item":deepcopy(item)}
                )

    def parse_url(self, response):
        item = response.meta["item"]
        tr_list = response.xpath("//div[@class='bdsub']/dl[@id='content']/dd[1]/table/tr[position()>1]")
        for tr in tr_list:
            item["name"] = tr.xpath("./td[1]/a[2]/text()").extract_first()
            item["address"] = tr.xpath("./td[1]/a[2]/@href").extract_first()
            item["new_chapter"] = tr.xpath("./td[2]/a/@href").extract_first()
            item["author"] = tr.xpath("./td[3]/text()").extract_first()
            item["w_count"] =tr.xpath("./td[4]/text()").extract_first()
            item["status"] = tr.xpath("./td[6]/text()").extract_first()
            if item["address"] is not None:
                yield scrapy.Request(
                    item["address"],
                    callback=self.get_url,
                    meta={"item":deepcopy(item)}
                )
        next_url = response.xpath("//a[text()='>']/a/@href").extract_first()
        if next_url is not None:
            scrapy.Request(
                next_url,
                callback=self.parse_url
            )

    def get_url(self, response):
        item = response.meta["item"]
        tr_list = response.xpath("//div[@class='bdsub']/dl/dd[3]/table/tr")
        for tr in tr_list:
            item["all_chapter"] = tr.xpath("./td/a/text()").extract_first()
            # URL = parse.urljoin(response.url, tr.xpath("./td/a/@href").extract_first())
            # item["chapter_add"] = URL
            item["chapter_add"] = response.urljoin(tr.xpath("./td/a/@href").extract_first())
            # print(item["chapter_add"])
            if item["chapter_add"] is not None:
                yield scrapy.Request(
                    item["chapter_add"],
                    callback=self.get_content,
                    meta={"item":deepcopy(item)}
                )

    def get_content(self, response):
        item = response.meta["item"]
        item["content"] = response.xpath("//dd[@id='contents']/text()").extract()
        # print(item["content"])
        return item
        # print(item)
