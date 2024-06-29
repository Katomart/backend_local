import requests

class RequestsBasedScrapper:

    DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0'}

    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)
        self.response = self.session.get(url)

    def set_headers(self, headers):
        self.session.headers.clear()
        self.session.headers.update(self.DEFAULT_HEADERS)
        self.session.headers.update(headers)

    def get_headers(self):
        return self.session.headers

    def set_cookies(self, cookies):
        self.session.cookies.clear()
        self.session.cookies.update(cookies)

    def get_cookies(self):
        return self.session.cookies

    def get_page(self):
        return self.response

    def post_page(self, data):
        self.response = self.session.post(self.url, data)
        return self.response

    def close(self):
        self.session.close()
