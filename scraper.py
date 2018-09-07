from bs4 import BeautifulSoup
import requests
from flask import Markup


class scraper():

    def __init__(self):
        self.booklist = []
        self.totaldata = 0
        self.target = ''

    def getData(self):
        return self.booklist

    def getProgress(self):
        try:
            return int(len(self.getData())*100//self.getTotalData())
        except ZeroDivisionError:
            return 0

    def getStatus(self):
        return self.getProgress() == 100

    def getTotalData(self):
        return self.totaldata

    def setTarget(self, data):
        self.booklist = []
        self.target = data

    def getTarget(self):
        return self.target

    def getPage(self, page):
        pagination = page.find('div', {'class': ['pagination clearfix']})
        try:
            pagelist = pagination.find_all('a')
            lastPage = pagelist[-1].contents[0]
        except AttributeError:
            return 1
        return int(lastPage)

    def getLinkList(self, lastpage):
        linkList = []
        for i in range(1, lastpage+1):
            url = "http://www.allitebooks.com/page/{}/?s={}".format(
                    i, self.getTarget())
            r = requests.get(url)
            page = BeautifulSoup(r.text, "html.parser")

            articleList = page.find_all('article')
            for book in articleList:
                linkList.append(book.find('a')['href'])
        self.totaldata = len(linkList)
        return linkList

    def getSubDescription(self, page, target):
        try:
            detail = page.find('dt', string='{}:'.format(target))
            return detail.find_next('dd').text
        except AttributeError:
            return None

    def getDescription(self, url):
        r = requests.get(url)
        page = BeautifulSoup(r.text, "html.parser")

        article = page.find('article')
        head = ['author',
                'ISBN-10',
                'Year',
                'Pages',
                'File size',
                'File format',
                'Category']
        data = {'details': {}}
        data['title'] = article.find('h1').contents[0]
        data['image'] = article.find('img')['src']
        data['description'] = [Markup(i) for i in article.find('div',
                                {'class': ['entry-content']}).contents]
        for key in head:
            data['details'][key] = self.getSubDescription(article, key)
        return data

    def isAvailable(self):
        url = "http://www.allitebooks.com/?s="+ self.getTarget()
        r = requests.get(url)
        page = BeautifulSoup(r.text, "html.parser")
        data = page.find('article')
        if data is None:
            return False
        else:
            return True

    def getBookList(self):
        url = "http://www.allitebooks.com/?s="+self.getTarget()
        r = requests.get(url)
        page = BeautifulSoup(r.text, "html.parser")
        if self.isAvailable() is False:
            yield str(-1)
        total_page = self.getPage(page)
        linkList = self.getLinkList(total_page)
        for link in linkList:
            self.booklist.append(self.getDescription(link))
            yield str(self.getProgress())
