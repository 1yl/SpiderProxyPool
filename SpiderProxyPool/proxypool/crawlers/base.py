from retrying import retry
import requests
from loguru import logger


class BaseCrawler(object):
    urls = []
    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None)  #  retry请求失败重试装饰器   # stop_max_attempt_number：在停止之前尝试的最大次数，最后一次如果还是有异常则会抛出异常，停止运行，默认为5次 | retry_on_result：指定一个函数，如果指定的函数返回True，则重试，否则抛出异常退出
    def fetch(self, url, **kwargs):
        try:
            response = requests.get(url, **kwargs)  # 请求指定url
            if response.status_code == 200: # 请求响应码返回为200
                return response.text    # 返回响应文本内容
        except requests.ConnectionError:
            return
    
    @logger.catch
    def crawl(self):
        """
        crawl main method
        """
        for url in self.urls:
            logger.info(f'fetching {url}')
            html = self.fetch(url)
            for proxy in self.parse(html):
                logger.info(f'fetched proxy {proxy.string()} from {url}')
                yield proxy
