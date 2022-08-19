import requests
from bs4 import BeautifulSoup


def connect_site(HEADERS):
    # подключаемся и сохраняем в переменную текст
    response = requests.get('https://habr.com/ru/all/', headers=HEADERS)
    text = response.text

    # отдаем текст и указываем что работаем с html
    soup = BeautifulSoup(text, features='html.parser')

    return soup


def search_articles(soup, KEYWORDS):
    # ищем статьи
    articles = soup.find_all('article', {'class': 'tm-articles-list__item'})

    for article in articles:
        # теги в статье
        hubs = article.find_all(class_='tm-article-snippet__hubs-item')
        hubs = [hub.find('a').text.strip(' *') for hub in hubs]

        # название статьи
        article_tag_a = article.find('a', class_='tm-article-snippet__title-link')
        article_name = article_tag_a.text

        # дата статьи
        dates = article.find('time')['title']

        # ссылка на статью
        href = article_tag_a.attrs['href']
        url = 'https://habr.com' + href

        # превью текста статьи (2 версии)
        preview_texts = article.find_all('div',
                                         class_='article-formatted-body article-formatted-body article-formatted-body_version-1')
        preview_texts2 = article.find_all('p')

        preview_text = (hubs, article_name, preview_texts, preview_texts2)

        # ищем в статье ключевые слова
        result = []
        for word in KEYWORDS:
            for text in preview_text:
                if word in text:
                    y = f'{dates[:11]} {article_name} {url}'
                    if not y in result:
                        result.append(y)

        for x in result:
            if not len(x) == 0:
                print(x)


if __name__ == '__main__':
    HEADERS = {'cept': '*/*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'ru,en;q=0.9',
               'Connection': 'keep-alive',
               'Cookie': 'feature_streaming_comments=true; hl=ru; connect_sid=s%3Avzkm1Mlkly6ZbPM3TrDOnUQmMhrDvTIZ.Gs5AAtyRUs%2B0ab%2Fj4UUd8nchvifolM9Zo%2FwZrO6r%2B74; fl=ru; visited_articles=597999:531472:488054:593707:536814:164325:670250:488782:227377:50147; _ym_d=1660633730; habr_web_home_feed=/all/',
               'DNT': '1',
               'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Yandex";v="22"',
               'sec-ch-ua-mobile': '?0',
               'sec-ch-ua-platform': "Windows",
               'Sec-Fetch-Dest': 'empty',
               'Sec-Fetch-Mode': 'cors',
               'Sec-Fetch-Site': 'same-origin',
               'sec-gpc': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.3.822 Yowser/2.5 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'
               }
    KEYWORDS = ['Python', 'анализ', 'Ноутбуки']

    soup = connect_site(HEADERS)
    search_articles(soup, KEYWORDS)
