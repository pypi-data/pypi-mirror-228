from LatestValidProxies.Spiders import IhuanSpider

if __name__ == '__main__':
    beesproxy_spider = IhuanSpider(show_logs=True)
    proxy = beesproxy_spider.get_one_useful_proxy()
    print(proxy.ip, proxy.port)
