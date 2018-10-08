# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import urlparse
import re
from zsy_scrapy.items import ArticleItem
from zsy_scrapy.util import common
from scrapy.loader import ItemLoader
import requests
import base64


# 获取每个文章的详细内容
def parse_detail(response):
    item_loader = ItemLoader(item=ArticleItem(), response=response)
    # title = response.xpath('//div[contains(@class, "newsTitle")]')
    title = response.xpath('//*[@id="ctl00_PlaceHolderMain_Title__ControlWrapper_RichHtmlField"]//h1')
    # if len(title) == 0:
    #     title = response.xpath('//span[contains(@class, "newsTitle")]')
    content = "".join(response.xpath('//*[@id="ctl00_PlaceHolderMain_Content__ControlWrapper_RichHtmlField"]//p').extract()).encode("utf8")
    images = response.xpath('//*[@id="ctl00_PlaceHolderMain_Content__ControlWrapper_RichHtmlField"]//img/@src').extract()
    medias = response.xpath('//*[@id="MediaPlayer"]//param[2]/@value').extract()
    # 下载视频
    if len(medias) > 0:
        for media in medias:
            media = media
            result_value = requests.get(media).content
            with open((media[media.rfind("/"):][2:]), 'wb') as f:
                f.write(result_value)
    # 替换所有图片为BASE64
    if len(images) > 0:
        for image in images:
            image = image.encode("utf8")
            image_all = "http://www.riped.petrochina" + image
            result = requests.get(image_all)
            base64_data = base64.b64encode(result.content)
            content = content.replace(image, base64_data)
    # 存取字段
    item_loader.add_value("title", str(title.xpath('string(.)').extract_first()).strip())
    item_loader.add_value("content", content)
    item_loader.add_value("url", response.url)
    item_loader.add_value("md5_url", common.get_md5(response.url))
    article_item = item_loader.load_item()
    yield article_item


# 主类
class ArticlespiderSpider(scrapy.Spider):
    name = 'ArticleSpider'
    allowed_domains = ['http://www.riped.petrochina']
    # 爬取得模块：今日要闻
    # start_urls = ['http://eip.cnpc/zhlm/jrgz/jrgz/Pages/more.aspx/']
    # 研究院要闻
    start_urls = ['http://www.riped.petrochina/riped/gdtpxw/Pages/index.aspx']

    def parse(self, response):
        # 列表文章的所有href
        post_urls = response.xpath('//*[@id="ctl00_PlaceHolderMain_g_56180fb8_7aa8_4d2f_bfab_cf7c30b1387b"]'
                                   '/div[1]/div/div[2]/ul//li/span[1]//a/@href').extract()
        for post_url in post_urls:
            # 防止href里属性值为uri 拼接url
            url1 = urlparse.urljoin(response.url, post_url)
            # 再次发送请求 因为url变了加入dont_filter=true（也可以在allowed_domains加入）
            yield Request(url1, callback=parse_detail, dont_filter=True)
        # 页面抓取的http请求手动拼接（页面没找到）
        next_url = "http://www.riped.petrochina/riped/gdtpxw/Pages/index.aspx?activepage="
        # 找到下一页的脚标
        num = response.xpath('//div[contains(@class, "StaticPublishing")]/span[last()]/a/@href').extract_first()
        # 拼接并再次递归
        if num:
            num = re.findall('\d+', num.encode("utf8"))[0]
            # 先爬取前两页
            if int(num) < 3:
                next_url = next_url + num
                if next_url:
                    yield Request(next_url, callback=self.parse, dont_filter=True)
