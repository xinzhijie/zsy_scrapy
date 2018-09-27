# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import urlparse
import re
from zsy_scrapy.items import ArticleItem
from zsy_scrapy.util import common
from scrapy.loader import ItemLoader


# 获取每个文章的详细内容
def parse_detail(response):
    item_loader = ItemLoader(item=ArticleItem(), response=response)
    title = response.xpath('//div[contains(@class, "newsTitle")]')
    item_loader.add_value("title", title.xpath('string(.)').extract_first().encode('utf8').strip().replace("\n", "").replace("\r", "").replace("\t", ""))
    item_loader.add_xpath("content", '//*[@id="ctl00_PlaceHolderMain_Content__ControlWrapper_RichHtmlField"]//p')
    item_loader.add_value("url", response.url)
    item_loader.add_value("md5_url", common.get_md5(response.url))
    article_item = item_loader.load_item()
    yield article_item


# 主类
class ArticlespiderSpider(scrapy.Spider):
    name = 'ArticleSpider'
    allowed_domains = ['http://www.riped.petrochina']
    # 爬取得模块：今日要闻
    start_urls = ['http://eip.cnpc/zhlm/jrgz/jrgz/Pages/more.aspx/']

    def parse(self, response):
        # 列表文章的所有href
        post_urls = response.xpath('//*[@id="ctl00_ctl28_g_4139630b_e2b6_46ad_9adf_c0052ad655cf"]'
                                   '/div[1]/div/div[2]/ul//li/span[1]//a/@href').extract()
        for post_url in post_urls:
            # 防止href里属性值为uri 拼接url
            url1 = urlparse.urljoin(response.url, post_url)
            # 再次发送请求 因为url变了加入dont_filter=true（也可以在allowed_domains加入）
            yield Request(url1, callback=parse_detail, dont_filter=True)
        # 页面抓取的http请求手动拼接（页面没找到）
        next_url = "http://eip.cnpc/zhlm/jrgz/jrgz/Pages/more.aspx?activepage="
        # 找到下一页的脚标
        num = response.xpath('//div[contains(@class, "w_newslistpage_pager")]/span[last()]/a/@href').extract_first()
        # 拼接并再次递归
        if num:
            num = re.findall('\d+', num.encode("utf8"))[0]
            if int(num) < 2:
                next_url = next_url + num
                if next_url:
                    yield Request(next_url, callback=self.parse, dont_filter=True)
