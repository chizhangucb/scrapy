# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class DangdangPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect("localhost", "root", "my_password", "ddbooks", charset='utf8')

        for i in range(0, len(item["title"])):
            title = item["title"][i]
            link = item["link"][i]
            comment = item["comment"][i]
            sql = "insert into dangdang(title, link, comment) values('"+title+"', '"+link+"', '"+comment+"')"
            conn.query(sql)
            conn.commit()
        conn.close()
        
        return item
