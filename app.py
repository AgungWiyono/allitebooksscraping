from flask import Flask
from flask import render_template, flash, request, Response, jsonify
from flask_paginate import Pagination
from scraper import scraper
from pagination import pagination
import time

app = Flask(__name__)
scrapedata = scraper()
paginatee = pagination()


def get_book(page, per_page):
    start = per_page*(page-1)
    return scrapedata.getData()[start:start+per_page]


@app.route('/tes')
def tes():
    data = scrapedata.getDescription(
                'http://http://www.allitebooks.com/pro-android-with-kotlin/')
    return data['description']


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    target = request.args.get('target')
    if (target is None or target == ''):
        return render_template('index.html',
                                do=False,
                                status=False)
    elif target != scrapedata.getTarget():
        scrapedata.setTarget(target)
        paginatee.setPage(1)
        return render_template('index.html',
                               status=scrapedata.getStatus(),
                               do=True
                               )
    else:
        paginatee.setPage(int(request.args.get('page', 1)))
        return render_template('index.html',
                               status=True,
                               do=False
                               )


@app.route('/proccess')
def proccess():
    def generate():
        for progress in scrapedata.getBookList():
            if scrapedata.isAvailable() is False:
                while(True):
                    yield "data:-1\n\n"
            yield "data:" + progress + "\n\n"
    paginatee.setTotal(scrapedata.getTotalData())
    return Response(generate(), mimetype='text/event-stream')


@app.route('/get-content')
def getContent():
    pagination_books = get_book(paginatee.page, paginatee.per_page)
    page = paginatee.page
    total = len(scrapedata.booklist)
    href = "/?target={}".format(scrapedata.getTarget())+"&page={0}"
    pagination = Pagination(
                    page=page,
                    per_page=5,
                    href=href,
                    total=total,
                    css_framework='bootstrap4'
                    )
    return jsonify({'data':
                    render_template('_book.html',
                                    data=pagination_books,
                                    page=page,
                                    per_page=5,
                                    pagination=pagination,
                                    )})


if __name__ == "__main__":
    app.run(debug=True)
