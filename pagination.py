from flask_paginate import Pagination

class pagination(object):

    def __init__(self):
        self.page = 1
        self.per_page = 5
        self.total = 10

    def setPage(self,page):
        self.page = page

    def setTotal(self, total):
        self.total = total

    def getPaginatee(self):
        return self.page, self.per_page, Pagination(
                                        page = self.page,
                                        per_page = self.per_page,
                                        total = self.total,
                                        css_framework = 'bootstrap4'
                                        )
