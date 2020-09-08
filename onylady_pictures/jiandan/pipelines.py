# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import urllib
import scrapy
import json
import codecs
from scrapy.exceptions import DropItem
#from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.pipelines.images import ImagesPipeline
from jiandan import settings


class JiandanPipeline(object):  #用来自定义图片存储
    def __init__(self):
        #title是中文，需转码
        #当运行scrapy crawl onlylady -o items.json后,数据默认保存为items.json,里面中文全为Unicode,重新打开或创建一个文件'jiandan.json',名称随意
        self.file = codecs.open('jiandan.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

class JiandanPipeline(ImagesPipeline):  # 继承ImagesPipeline这个类，实现这个功能
    def get_media_requests(self, item, info):  # 重写ImagesPipeline  get_media_requests方法
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url,meta={'item':item})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
            #item['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):  #自定义存储路径
        item = request.meta['item']  # 通过上面的meta传递过来item
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(item['title'], image_guid)  #title为二级目录
        return filename
