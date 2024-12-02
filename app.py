import os
from datetime import datetime
from typing import List

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
from sqlitedb import IndexedDBManager

load_dotenv()
NEWS_API_KEY = os.environ['NEWS_API_KEY']

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
db = IndexedDBManager('db.sqlite3')


def perform_search(search_query: str):
    articles = requests.get('https://newsapi.org/v2/everything',
                            params={'q': search_query, 'apiKey': NEWS_API_KEY}).json()
    db['searches'][search_query] = {
        'search_query': search_query,
        'searched_at': datetime.now().isoformat(),
        'articles': articles
    }


def get_saved_search_queries() -> List[str]:
    return list(map(
        lambda x: x['search_query'],
        sorted(db['searches'].values(), key=lambda x: datetime.fromisoformat(x['searched_at']), reverse=True)
    ))


@app.route('/', methods=['GET', 'POST'])
def page_home():
    search_query = request.args.get('search', '')
    search = None
    search_new = False
    if search_query:
        if search_query not in db['searches'] or request.args.get('action', '') == 'force-refresh':
            perform_search(search_query)
            search_new = True
        search = db['searches'][search_query]
        search['articles']['articles'] = sorted(
            search['articles']['articles'],
            key=lambda x: datetime.fromisoformat(x['publishedAt']), reverse=True
        )

    return render_template(
        'base.html',
        search_query=search_query,
        search=search,
        saved=get_saved_search_queries(),
        search_new=search_new
    )


if __name__ == '__main__':
    app.run()
