from LatestValidProxies.Spiders import BeesProxySpider

if __name__ == '__main__':
    b = BeesProxySpider()
    print(b.get_one_useful_proxy().__dict__)
