from concurrent.futures import ThreadPoolExecutor, as_completed
from .SpiderConfiger import SpiderConfiger
import requests
from fake_useragent import UserAgent
from lxml import etree
from datetime import datetime
from .Proxy import Proxy
import time
import json
from .log import logger
import sys


class Spider(object):
    def __init__(self, urls, group_xpath, detail_xpath, spider_configer=SpiderConfiger()):
        self.urls = urls
        self.group_xpath = group_xpath
        self.detail_xpath = detail_xpath
        self.spider_configer = spider_configer
        self.to_end = False

    def get_proxies_from_one_page(self, url):
        logger.info(f'正在尝试与 {url} 建立连接')
        headers = {
            'User-Agent': UserAgent().random
        }
        response = requests.get(url, headers=headers)
        page = response.content
        parser = etree.HTMLParser(encoding=self.spider_configer.encoding)
        html = etree.HTML(page, parser=parser)
        trs = html.xpath(self.group_xpath)
        proxies = []
        logger.info('正在收集网页代理ip信息')
        for tr in trs:
            ip = tr.xpath(self.detail_xpath['ip'])[0].strip()
            port = tr.xpath(self.detail_xpath['port'])[0].strip()
            area = tr.xpath(self.detail_xpath['area'])[0].strip()
            obtain_time = datetime.now().strftime(self.spider_configer.datetime_format)
            proxies.append(Proxy(ip, port, -1, area, url, obtain_time))
        return proxies

    def test(self, test_url, proxy):
        headers = {
            'User-Agent': UserAgent().random
        }
        proxies = {
            'http': f'http://{proxy.ip}:{proxy.port}',
            'https': f'http://{proxy.ip}:{proxy.port}'
        }
        start = time.time()
        try:
            if self.to_end:
                return False, Proxy()
            response = requests.get(
                url=test_url,
                headers=headers,
                proxies=proxies,
                timeout=self.spider_configer.test_timeout
            )
            if response.ok:
                proxy.speed = round(time.time() - start, 2)
                content = response.text
                content_dic = json.loads(content)
                origin = content_dic['origin']
                if ',' not in origin:
                    return True, proxy
        except Exception:
            return False, Proxy()
        return False, Proxy()

    def test_proxy(self, proxy):
        if self.to_end:
            return Proxy()
        logger.info(f'正在检测代理ip: {proxy.ip}:{proxy.port}')
        http_check, http_proxy = self.test('http://httpbin.org/get', proxy)
        https_check, https_proxy = self.test('https://httpbin.org/get', proxy)
        if https_check:
            return https_proxy
        if http_check:
            return http_proxy
        return Proxy()

    def get_one_useful_proxy(self):
        start = time.time()
        self.to_end = False
        for url in self.urls:
            proxies = self.get_proxies_from_one_page(url)
            # logger.info(f'正在检测来自 {url} 的代理ip')
            with ThreadPoolExecutor(max_workers=self.spider_configer.max_worker) as pool:
                futures = [pool.submit(self.test_proxy, proxy) for proxy in proxies]
                for future in as_completed(futures):
                    proxy = future.result()
                    if proxy.speed != -1:
                        logger.info(f'找到有效的匿名代理ip: {proxy.ip}:{proxy.port}')
                        self.to_end = True
                        end = time.time()
                        logger.info(f'本次抓取代理ip耗时: {round(end - start, 2)} s, 正在等待其他线程的结束, 预计耗时0~10s')
                        return proxy
        logger.warning('无法找到有效的匿名代理ip')
        end = time.time()
        logger.info(f'本次抓取代理ip耗时: {round(end - start, 2)} s, 正在等待其他线程的结束, 预计耗时0~10s')
        return Proxy

    def get_useful_proxies(self, count=sys.maxsize):
        start = time.time()
        self.to_end = False
        valid_proxies = []
        for url in self.urls:
            proxies = self.get_proxies_from_one_page(url)
            # logger.info(f'正在检测来自 {url} 的代理ip')
            with ThreadPoolExecutor(max_workers=self.spider_configer.max_worker) as pool:
                futures = [pool.submit(self.test_proxy, proxy) for proxy in proxies]
                for future in as_completed(futures):
                    proxy = future.result()
                    if proxy.speed != -1:
                        logger.info(f'找到有效的匿名代理ip: {proxy.ip}:{proxy.port}')
                        valid_proxies.append(proxy)
                        if len(valid_proxies) >= count:
                            self.to_end = True
        end = time.time()
        if len(valid_proxies):
            logger.info(f'本次抓取代理ip耗时: {round(end - start, 2)} s, 正在等待其他线程的结束, 预计耗时0~10s')
            return valid_proxies
        logger.warning('无法找到有效的匿名代理ip')
        logger.info(f'本次抓取代理ip耗时: {round(end - start, 2)} s, 正在等待其他线程的结束, 预计耗时0~10s')
        return []


if __name__ == '__main__':
    # start = time.time()
    # print(beesproxy_spider.get_one_useful_proxy().__dict__)
    # cost = round(time.time() - start, 2)
    # print(f'本次调用用时: {cost} s')

    # rsp = requests.get(
    #     url='http://httpbin.org/get',
    #     headers={'User-Agent': UserAgent().random},
    #     proxies={
    #         'http': 'http://202.110.67.141:9091',
    #         'https': 'http://202.110.67.141:9091',
    #     }
    # )
    # print(rsp.content.decode())
    pass
