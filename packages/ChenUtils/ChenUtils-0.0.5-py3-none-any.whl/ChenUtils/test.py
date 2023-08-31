import LatestValidProxies

if __name__ == '__main__':
    beesproxy_spider = LatestValidProxies.Spiders.BeesProxySpider(show_logs=True)
    proxy = beesproxy_spider.get_one_useful_proxy()
    print(proxy.ip, proxy.port)
