import scrapy


class GlSpider(scrapy.Spider):
    name = 'gl'
    # allowed_domains = ['guilin.com']
    start_urls = ['http://2shou.guilinlife.com/']

    def parse(self, response):
        links = response.xpath('//div[@class="items"]/ul//p/a/@href').getall()
        for link in links:
            yield response.follow(url=link, callback=self.parse_lists)

    def parse_lists(self, response):
        pages = response.xpath('//div[@id="pageList"]/div[@class="fr"]/a/@href').getall()
        if pages:
            for page in pages:
                yield response.follow(url=page, callback=self.parse_lists)

        print('next is infos')
        titles = response.xpath('//div[@id="listEach"]/ul//dl/dt/a/text()').getall()
        detail_pages = response.xpath('//div[@id="listEach"]/ul//dl/dt/a/@href').getall()
        introduces = response.xpath('//div[@id="listEach"]/ul//dl/dd[1]/text()').getall()

        nick_names = response.xpath('//div[@id="listEach"]/ul//dl/dd[2]/a/text()').getall()
        telephones = response.xpath('//div[@id="listEach"]/ul//dl/dd[2]/text()[2]').getall()
        for title, detail_page, introd, nick_name, telephone in zip(titles, detail_pages, introduces, nick_names, telephones):
            # print(title, introd)
            # print(detail_page)
            # print(nick_name, telephone)
            # print('*'*30)
            item = {}
            item['title'] = title
            item['introduce'] = introd
            item['detail_page'] = detail_page
            item['nick_name'] = nick_name
            item['telephone'] = telephone
            yield item

