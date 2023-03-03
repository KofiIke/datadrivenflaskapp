import requests
from datetime import datetime
from app import db, Article, Author

API_KEY = '904e63f9-ae5e-4a38-a4c9-91d72db06744'
API_URL = 'https://content.guardianapis.com/search'

def load_data():
    params = {
        'api-key': API_KEY,
        'from-date': '2021-01-01',
        'to-date': '2022-02-01',
        'page-size': 100
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    for result in data['response']['results']:
        author = Author.query.filter_by(email=result['fields'].get('bylineEmail')).first()

        if not author:
            author = Author(name=result['fields'].get('byline'), email=result['fields'].get('bylineEmail'))
            db.session.add(author)

        article = Article(
            title=result['webTitle'],
            author=author,
            publication_date=datetime.strptime(result['webPublicationDate'], '%Y-%m-%dT%H:%M:%SZ'),
            url=result['webUrl']
        )

        db.session.add(article)

    db.session.commit()
