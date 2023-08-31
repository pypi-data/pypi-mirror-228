from .Spider import Spider
from fake_useragent import UserAgent
from lxml import etree
import requests
from .SpiderConfiger import SpiderConfiger
import time


class BeesProxySpider(Spider):

    def __init__(self, spider_configer=SpiderConfiger(), show_logs=False):
        self.config = {
            'urls': [f'https://www.beesproxy.com/free/page/{page}' for page in range(1, spider_configer.max_pages + 1)],
            'group_xpath': '//*[@id="article-copyright"]/figure/table/tbody/tr',
            'detail_xpath': {
                'ip': './td[1]/text()',
                'port': './td[2]/text()',
                'area': './td[3]/text()'
            },
            'spider_configer': spider_configer,
            'show_logs': show_logs
        }
        super().__init__(**self.config)


class Ip89Spider(Spider):

    def __init__(self, spider_configer=SpiderConfiger(), show_logs=False):
        self.config = {
            'urls': [f'https://www.89ip.cn/index_{page}.html' for page in range(1, spider_configer.max_pages + 1)],
            'group_xpath': "//*[name()='tbody']/tr",
            'detail_xpath': {
                'ip': './td[1]/text()',
                'port': './td[2]/text()',
                'area': './td[3]/text()'
            },
            'spider_configer': spider_configer,
            'show_logs': show_logs
        }
        super().__init__(**self.config)


class KuaidailiSpider(Spider):

    def __init__(self, spider_configer=SpiderConfiger(), show_logs=False):
        self.config = {
            'urls': [f'https://www.kuaidaili.com/free/intr/{page}' for page in range(1, spider_configer.max_pages + 1)],
            'group_xpath': "//*[name()='tbody']/tr",
            'detail_xpath': {
                'ip': './td[1]/text()',
                'port': './td[2]/text()',
                'area': './td[5]/text()'
            },
            'spider_configer': spider_configer,
            'show_logs': show_logs
        }
        super().__init__(**self.config)


class Ip66Spider(Spider):

    def __init__(self, spider_configer=SpiderConfiger(), show_logs=False):
        self.config = {
            'urls': [f'http://www.66ip.cn/{page}.html' for page in range(1, spider_configer.max_pages + 1)],
            'group_xpath': "//*[name()='table']/tr[position()>1]",
            'detail_xpath': {
                'ip': './td[1]/text()',
                'port': './td[2]/text()',
                'area': './td[3]/text()'
            },
            'spider_configer': spider_configer,
            'show_logs': show_logs
        }
        super().__init__(**self.config)


class IhuanSpider(Spider):

    def __init__(self, spider_configer=SpiderConfiger(), show_logs=False):
        self.ihuan_pages = (self.get_ihuan_pages('https://ip.ihuan.me/?page=b97827cc') +
                            self.get_ihuan_pages('https://ip.ihuan.me/?page=eas7a436'))
        self.config = {
            'urls': [f'https://ip.ihuan.me/{page}' for page in self.ihuan_pages],
            'group_xpath': "//*[name()='tbody']/tr",
            'detail_xpath': {
                'ip': './td[1]/a/text()',
                'port': './td[2]/text()',
                'area': './td[3]/a/text()'
            },
            'spider_configer': spider_configer,
            'show_logs': show_logs
        }
        super().__init__(**self.config)

    def get_ihuan_pages(self, url) -> list[str]:
        response = requests.get(url, headers={'User-Agent': UserAgent().random})
        html = etree.HTML(response.content)
        pages = html.xpath("//*[name()='ul']/li[position()>1]/a/@href")[4:10]
        return pages


if __name__ == '__main__':
    beesproxy_spider = BeesProxySpider(show_logs=True)
    proxy = beesproxy_spider.get_one_useful_proxy()
    print(proxy.ip, proxy.port)
