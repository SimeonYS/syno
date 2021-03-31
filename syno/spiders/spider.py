import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import SynoItem
from itemloaders.processors import TakeFirst
from scrapy import Selector
import requests
import datetime

pattern = r'(\xa0)?'

url = "https://www.synovus.com/api/sitecore/NewsRoom/LoadNewsPressReleases"

payload = '{{"type": "news","year": "{}"}}'
headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Content-Type': 'application/json; charset=UTF-8',
    'Origin': 'https://www.synovus.com',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.synovus.com/about-us/news/',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cookie': 'ASP.NET_SessionId=cvmt13h1jnxdsrjnjyi4p5yq; SC_ANALYTICS_GLOBAL_COOKIE=01267211300c4ecfa9c41dfe17650336|False; SeoUserID=39261751-A045-4314-BBA7-F39C0427EB71; userId=; Syn_website=1969858752.20480.0000; bm_sz=F19E685190578F892D5B25FC8A64912A~YAAQnqwVAqJqgXZ4AQAApgsdhwuk94uFgdPsh+gvnB78BDsMi8i4sy0hkkDIOr4JK9tBhnbs18WLzndZ9i/7KeoQ5/DjA8ST5QOlgzwOoT0Ko1T04sD4OeIfgRUfluFIVP0UOoEZHTl5fVgBQxpTIrjrcEXjW8u8rmBVLuahjGEVriGwvKx4/DGSyrXkYV6+cMVCluBqp1lI4Gf+dT29YyShzM6OEvCeEyhZAo9IFjfBeWTvmnX9EEo7oMk+jOMh; _ga=GA1.2.723589880.1617174532; _gid=GA1.2.1098468566.1617174532; _gcl_au=1.1.353146705.1617174532; _fbp=fb.1.1617174534515.1066780486; bm_mi=A5C9F599C146D7E88720D2C27EBEB1B7~iIofR7BtBIlcnBPP12lI7BQDexDzImaIHoF9YhsPF0zAkyQJ10/Hh3ThpnEf8vfmqnSGQinv7/HRkzSHi/PsZ4eXd8eVs+lveauy6249K+K6GAet5QD1Jr0ONa85UplO1GLqEPsB9/C5EIvtCBszDEo1vcJzARkpDFNn7pIOfa0SqndZWJNfKvhRX6mzotwyHUVnlNa6GNwlqEfZsXC2bANWeaDQJxLrkbvjzTR6o4+DiAzSTuZ9PoS3Ma/IbOqJtzM2Ay/Es6qf7I8prQLkRgFHSKC9l2IDVXSBWKTP7+k=; ak_bmsc=6C1032212FD9D3E2F08D5FC6A8D39FB00215AC9E8073000002206460E9BD9116~pld6JjNlC8H1NOe6lAdYrPAEwKHBYczPy78oEYDp3l8Nua5R2vghDD+c3BpOu+ucdW8VNQTG7XFJCY4vZHCYaQb3nr58zEnkAmf5XbSGPR9upBHRuUiKx/KzWr/xmIJkgou/vZVzKdaLv7wCTeBQg/XM2geBac/jRG7xzn2n+8EdBC00mYp9S1HzMQB8JpGOeOqJ1wvbJyVZzbzoEdQGnT65uBE3IY1jDkF9vs2gXg+TMUHiKMSQ2vtAj0RcfNLTXM; _abck=C6996C578E7718B9B235818379B9A925~0~YAAQnqwVAk1rgXZ4AQAAJT0dhwViXfxRP4DGyMsmsII9Ldv9tM/6IXgogAhMg0dmYFPOfb95qfgAeDuFk8tRgLX35nJZsBUzqQDaFVjYgPzaxkjb4lLBff7fRemKxReXrDYd+t+ipKH34wi7wHtfwAEckX77tglWY9ZlI94yJJhAYpqCF61PFGUlc5MXd1utNNaktdTbEpXzFIjw1vqwp/KTRFuRTLi+DzfW/JJj44ua7EVjf7YZ1K144tyVZoO6fi7yyLNz8CPuGM692TpjU0mSarXAFiV3zfwpkP/m5mDGVZwndR+7uwoRLOj8CrafxSDxIxtUl4myqq0d98+0wbQjyqByWvI3DFnuNNwoZKmWinfnsqNVTJvi8jINL5BRvFBaO5Gf2v8Drpjyqj3xQnlc8KFcUFlFnA==~-1~-1~-1; __session:0.9341355427641163:=https:; NewsType=news; NewsYear=2019; bm_sv=9AA5B8F3697A51DFEE5DE57DE31A7477~e2Krcu9/YQAm99FBHZjQXyfvTXO5WeW0af+cAoMXCs+ehvbEGWFgQ98B9S/xkDmLdAPB20OXpAkZdNyUM1rWIOw8OqTkckdBRmVd1mE2SREfhgf2W2TXjFUpQdT/f7WJroOtJdqQ2nQv0AWeyzlofZJA70ro8Af9NV2PR+y7hFA=; _abck=C6996C578E7718B9B235818379B9A925~-1~YAAQnqwVAkF6gXZ4AQAAcbMghwW0j4Tzzf6tOwS2zjKCcEO0+MU84MgExhKu+U80Sds4vyvoEbpfrr1GbgRfjfEGEo4TDWOHxwozbsouBahkWCzhGt8gQy2cdUOb2+ZQafx3w0szb5jDpoT6PR1zVA7W7lDQc2SMgpxsOFdyq1Nh8mqAo4qyZDjdKwPIuadFupw60qdnfu58YPwmGKttwx2uKcxVEizs80mF127KQDk1dFIh4heJhdo8ldVMuq8oem9Gb9xW6fmniJCfKs9rsw48Vf/ZSKVFYLhcubJSwwVsmpHMC1vxHb8fugpt8gquAg9G1jXWacvuCFpis3LgxU1uWEzUFOCjqh2m99NNn4UiTD6oftlWAg+O3BHmYbU9AJRjGVpxXTDzRI0jYb26dCDO25n1aG+BNg==~0~-1~-1; bm_sv=9AA5B8F3697A51DFEE5DE57DE31A7477~e2Krcu9/YQAm99FBHZjQXyfvTXO5WeW0af+cAoMXCs+ehvbEGWFgQ98B9S/xkDmLdAPB20OXpAkZdNyUM1rWIOw8OqTkckdBRmVd1mE2SRF+xA+MYEAHz9wD0W/gadw2gdI32wF8bKnCBZWAOsO86OrSuHj2rDgitsi5cBBbkmc=; NewsType=news; NewsYear=2021'
}

class SynoSpider(scrapy.Spider):
    name = 'syno'
    now = datetime.datetime.now()
    year = now.year
    start_urls = ['https://www.synovus.com/about-us/news/']

    def parse(self, response):
        data = requests.request("POST", url, headers=headers, data=payload.format(self.year))
        posts = Selector(text=data.text).xpath('//a[@class="article"]')
        for post in posts:
            date = post.xpath('.//span[@class="article-date"]/text()').get()
            links = post.xpath('.//@href').get()
            yield response.follow(links, self.parse_post, cb_kwargs=dict(date=date))

        if self.year >= 2016:
            self.year -= 1
            yield response.follow(response.url, self.parse, dont_filter=True)

    def parse_post(self, response, date):
        title = response.xpath('//h1/text()').get().strip()
        content = response.xpath('//div[@class="news-page"]//text()[not (ancestor::h1)]').getall()
        content = [p.strip() for p in content if p.strip()]
        content = re.sub(pattern, "",' '.join(content))

        item = ItemLoader(item=SynoItem(), response=response)
        item.default_output_processor = TakeFirst()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)
        item.add_value('date', date)

        yield item.load_item()
