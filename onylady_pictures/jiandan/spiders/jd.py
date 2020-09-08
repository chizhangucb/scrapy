import scrapy
from jiandan.items import JiandanItem
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse,Request
import logging  #写不写都行，用来把log写入文件file_name


class JdSpider(scrapy.Spider):
    name = 'onlylady'
    allowed_domains = ['onlylady.com']
    start_urls = ["http://pic.onlylady.com/cate-10004_50_3.shtml",
                  "http://pic.onlylady.com/cate-10009_50_3.shtml",
                  "http://pic.onlylady.com/cate-10011_50_3.shtml",
                  "http://pic.onlylady.com/cate-10060_50_3.shtml"]  #初始的url，scrapy很方便强大吧

    def parse(self, response):
        imageurl=[]
        item = JiandanItem()

        # 根据xpath获取title，此处 ''.join()是为了在后面为图片自定义名称时使用,若不加''.join(),后面调用item['title']会得到Unicode码
        item['title']=''.join(response.xpath('//head/title/text()').extract()[0])

        imageurl = response.xpath('//img/@src').extract()  # 提取图片链接
        item['image_urls']=[i.replace('375x375','985x695') for i in imageurl]  #小图转大图链接
        # print 'image_urls',item['image_urls']
        yield item
        n_url = response.xpath('//a[@class="n"]//@href').extract_first()  # 翻页
        new_url = "http://pic.onlylady.com/" + str(n_url)  #构造出下页的url

        # print 'new_url', new_url
        if new_url:
            #根据scrapy爬虫流程，回调函数用来把new_url传到调度器生成request
            yield scrapy.Request(new_url, callback=self.parse)
           # self.log("your log information")
