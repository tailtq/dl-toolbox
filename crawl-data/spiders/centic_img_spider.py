import scrapy
import cv2

index = 0

class CenticImgSpider(scrapy.Spider):
    name = 'images'
    domain = 'http://camera.centic.vn'

    def start_requests(self):
        urls = []

        for i in range(1, 64):
            urls.append('http://camera.centic.vn/vipham/index/page:{}'.format(i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        detail_pages = response.css('td.clickable-row::attr(data-href)').getall()

        for detail_page in detail_pages:
            # self.index += 1
            yield scrapy.Request(url=self.domain + detail_page, callback=self.parse_detail)

    def parse_detail(self, response):
        global index
        video = self.domain + response.css('video::attr(src)').get()

        capture = cv2.VideoCapture(video)
        _, frame = capture.read()
        index += 1
        cv2.imwrite('data/data_street/' + str(index).rjust(7, '0') + '.jpg', frame)
        capture.release()
