import datetime
import os

import lxml.html as html
import requests

HOME_URL = ''

XPATH_LINK_TO_ARTICLE = '//div[contains(@class, "V")]/a[contains(@class, "kicker")]/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/h2/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not (@class)]/text()'


def parse_notice(link, today):
    try:
        response = requests.get(link)

        if response.status_code != 200:
            raise ValueError(f'Error: {response.status_code}')

        notice = response.content.decode('utf-8')
        parsed = html.fromstring(notice)

        try:
            title = parsed.xpath(XPATH_TITLE)[0]
            title = title.replace('\"', '').strip()

            summary = parsed.xpath(XPATH_SUMMARY)[0]
            body = parsed.xpath(XPATH_BODY)
        except IndexError:
            return

        with open(f'news/{today}/{title}.txt', 'w', encoding = 'utf-8') as f:
            f.write(title)
            f.write('\n\n')
            f.write(summary)
            f.write('\n\n')

            for p in body:
                f.write(p)
                f.write('\n')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)

        if response.status_code != 200:
            raise ValueError(f'Error: {response.status_code}')

        home = response.content.decode('utf-8')
        parsed = html.fromstring(home)
        links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
        # print(links_to_notices)

        today = datetime.date.today().strftime('%Y-%m-%d')
        news_dir = f'news/{today}'

        if not os.path.isdir('news'):
            os.mkdir('news')

        if not os.path.isdir(news_dir):
            os.mkdir(news_dir)

        for link in links_to_notices:
            parse_notice(link, today)
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()
