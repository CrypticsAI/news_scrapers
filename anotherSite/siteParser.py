import time
import logging
import csv
import json
import re
import os.path
import threading
from datetime import date, datetime, timezone
import requests
from requests.exceptions import RequestException
import bs4

import altcointoday.config as config

logging.basicConfig(filename='parser.log',
                    level=logging.INFO,
                    format="%(asctime)s:%(levelname)s:%(message)s")

class parser_thread(threading.Thread):
    #Класс потока парсера
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        start_parse(self.name)

def make_request(url):
    #выполняет запрос
    try:
        response = requests.get(url,headers=config.HEADERS)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        logging.error('Request error on url %s' % url)
        return None

def get_html(html):
    #обрабатывает ответ и возвращает bs4 объект
    if html:
        result = bs4.BeautifulSoup(html, 'lxml')
        return result
    else:
        logging.error('Empty response')
        return None

def get_links(html,link_set,par):
    #получает список ссылок на статьи
    tag = par['links_to_art']['tag']
    attr = par['links_to_art']['attr']
    attr_value = par['links_to_art']['attr_value']
    short_link = par['short_link']
    urls = []
    to_save = []
    #ищет все теги со ссылками по шаблону
    links = html.findAll(tag, {attr: attr_value})
    if links:
        for link in links:
            #проверка является ли ссылка сслыкой на текущий сайт
            same_site = re.match(par['browse_url'],link.a['href'])
            if short_link:
                urls.append(link.a['href'][1:])
            elif same_site:
                url = config.link_pattern.findall(link.a['href'])
                urls.append(url[0])
            else:
                continue
    urls = list(set(urls) - link_set) #выбор новых статей
    for url in urls:
            time.sleep(1)
            to_save.append(parse_article(url, par))
            #to_save.append(parse_article(url, par, fullurl=False))
    #сохранение результатов в csv
    write_csv(to_save, par)

# start для всех остальных, постраничного парсинга urls
def parse_article(url,par):
    #парсит статью
    url = ''.join([par['browse_url'],url])
    result = []
    article = get_html(make_request(url))
    raw_str_text = get_text(article, par)
    clean_str_text = re.sub(r'(\s{2,})|\A(\')|\b(\')|(\\n)|(\\xa0)|(")|("")|\'"|"', ' ', repr(raw_str_text))
    clean_str_title = re.sub(r'\A(\')|\b(\')', '', get_title(article, par))
    clean_author = re.sub(r'\APosted\sby\s', '', get_author(article, par))
    clean_str_url = re.sub(r'https:\/\/www.coindesk.com', '', url)
    clean_date_time = re.search(r'\d{4}-\d{2}-\d{2}\D\d{2}:\d{2}:\d{2}', get_date_time(article,par))
    # clean_views = re.sub(r'\s\s\sTotal\sviews', '', get_views(article, par))
    # clean_shares = re.sub(r'\sTotal\sshares', '', get_shares(article, par))

    date_time_timestamp = int(datetime.strptime(clean_date_time.group(0), "%Y-%m-%dT%H:%M:%S").timestamp())
    #date_time_timestamp = datetime.strptime(get_date_time(article,par), "%Y-%m-%d %H:%M:%S").timestamp()
    # date_time_timestamp = int(datetime.strptime(get_date_time(article,par), "%Y-%m-%d %H:%M:%S").timestamp()) # , tzinfo=datetime.timezone.utc
    #time.mktime(datetime.strptime(get_date_time(article,par), "%Y-%m-%d %H:%M:%S").timetuple())

    if article:
        #result.append(date.today())
        result.append(int(datetime.today().timestamp()))
        # result.append(repr(get_date_time(article,par)))
        result.append(repr(date_time_timestamp)) #(article,par)))
        # result.append(repr(get_author(article, par)))
        result.append(clean_author)
        #result.append(repr(url))
        result.append(clean_str_url)
        result.append(repr(get_views(article, par)))
        # result.append(clean_views)
        result.append(repr(get_shares(article, par)))
        # result.append(clean_shares)
        result.append(repr(get_likes(article, par))) # у cointelegraph нет лайков статей
        # result.append(repr(get_title(article,par)))
        result.append(clean_str_title)
        # result.append(repr(get_text(article,par)))
        result.append(clean_str_text)
        return result
    else:
        return None # end для всех остальных, постраничного парсинга urls


#start для Cointelegraph, постатейного парсинга urls_art
# def parse_article(url, par, fullurl=False):
#     #парсит статью
#         if not fullurl:
#             url = ''.join([par['browse_url'], url])
#         result = []
#         article = get_html(make_request(url))
#         raw_str_text = get_text(article,par)
#         clean_str_text = re.sub(r'(\s{2,})|\A(\')|\b(\')|(\\n)|(\\xa0)|(")|("")|\'"|"', ' ', repr(raw_str_text))
#         clean_str_title = re.sub(r'\A(\')|\b(\')', '', get_title(article, par))
#         clean_author = re.sub(r'\A(\')|\b(\')', '', get_author(article, par))
#         clean_str_url = re.sub(r'(https:\/\/)|(www.)', '', url)
#         clean_views = re.sub(r'\s\s\sTotal\sviews', '', get_views(article, par))
#         clean_shares = re.sub(r'\sTotal\sshares', '', get_shares(article, par))
#
#         # парсинг даты статьи из json
#         # date_time_timestamp = datetime.strptime(get_date_time(article,par), "%Y-%m-%d %H:%M:%S").timestamp()
#         # date_time_timestamp = int(datetime.strptime(get_date_time(article, par), "%Y-%m-%d %H:%M:%S").timestamp())
#
#         # парсинг даты статьи если json с ошибками.
#         date_time_find = re.search(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', (get_date_time(article,par)))
#         date_time_timestamp = int(datetime.strptime(date_time_find.group(0), "%Y-%m-%d %H:%M:%S").timestamp())

#
#         # date_time_timestamp = int(datetime.strptime(date_time_find), "%Y-%m-%d %H:%M:%S").timestamp()
#         #, tzinfo=datetime.timezone.utc
#         # time.mktime(datetime.strptime(get_date_time(article,par), "%Y-%m-%d %H:%M:%S").timetuple())
#
#
#         if article:
#             # result.append(date.today())
#             result.append(int(datetime.today().timestamp()))
#             # result.append(repr(get_date_time(article,par)))
#             result.append(repr(date_time_timestamp))  # (article,par)))
#             # result.append(repr(get_author(article, par)))
#             result.append(clean_author)
#             # result.append(repr(url))
#             result.append(clean_str_url)
#             # result.append(repr(get_views(article, par)))
#             result.append(clean_views)
#             # result.append(repr(get_shares(article, par)))
#             result.append(clean_shares)
#             result.append(repr(get_likes(article, par)))  # у cointelegraph нет лайков статей
#             # result.append(repr(get_title(article,par)))
#             result.append(clean_str_title)
#             # result.append(repr(get_text(article,par)))
#             result.append(clean_str_text)
#             return result
#         else:
#             return None # end для Cointelegraph, постатейного парсинга urls_art

def get_title(html,par):
    # возвращает заголовок статьи
    tag = par['title']['tag']
    attr = par['title']['attr']
    attr_value = par['title']['attr_value']
    #поиск тэга с заголовком заданным в config
    head = html.find(tag,{attr: attr_value})
    try:
        return head.text.strip()
    except AttributeError:
        logging.error('title not found')
        return None

# парсинг даты статьи если json с ошибками.
def get_date_time(html,par):
    # возвращает время написания статьи
    tag = par['date_time']['tag']
    attr = par['date_time']['attr']
    attr_value = par['date_time']['attr_value']
    # поиск тэга с заголовком заданным в config
    head = html.findAll(tag, {attr: attr_value})
    try:
        return head[1]['content']
    except AttributeError:
        logging.error('date_time not found')
        return None

# парсинг даты статьи из json
# def get_date_time(html,par):
#     # возвращает время написания статьи
#     tag = par['date_time']['tag']
#     attr = par['date_time']['attr']
#     attr_value = par['date_time']['attr_value']
#     # поиск тэга с заголовком заданным в config
#     head = html.find(tag, {attr: attr_value})
#     val = json.loads(head.text)
#     result = val['dateModified']
#
#     try:
#         return result
#     except AttributeError:
#         logging.error('date_time not found')
#         return None

def get_author(html,par):
    # возвращает автора статьи
    tag = par['author']['tag']
    attr = par['author']['attr']
    attr_value = par['author']['attr_value']
    # поиск тэга с заголовком заданным в config
    head = html.find(tag, {attr: attr_value})
    try:
        return head.text.strip()
    except AttributeError:
        logging.error('author not found')
        return None

def get_views(html,par):
    # возвращает просмотры статьи
    tag = par['views']['tag']
    attr = par['views']['attr']
    attr_value = par['views']['attr_value']
    # поиск тэга с заголовком заданным в config
    head = html.find(tag, {attr: attr_value})
    try:
        return head.text.strip()
    except AttributeError:
        logging.error('views not found')
        return None

def get_shares(html,par):
    # возвращает shares статьи
    tag = par['shares']['tag']
    attr = par['shares']['attr']
    attr_value = par['shares']['attr_value']
    # поиск тэга с заголовком заданным в config
    head = html.find(tag, {attr: attr_value})
    try:
        return head.text.strip()
    except AttributeError:
        logging.error('shares not found')
        return ''

def get_likes(html,par):
    # возвращает лайки статьи
    tag = par['likes']['tag']
    attr = par['likes']['attr']
    attr_value = par['likes']['attr_value']
    # поиск тэга с заголовком заданным в config
    head = html.find(tag, {attr: attr_value})
    try:
        return head.text.strip()
    except AttributeError:
        logging.error('likes not found')
        return None

def get_text(html,par): # get_text clean_str_text(html,par):
    #возвращает текст статьи
    tag = par['body']['tag']
    attr = par['body']['attr']
    attr_value = par['body']['attr_value']
    result = []
    #поиск тэга с телом статьи
    text_tags = html.find(tag,{attr: attr_value})
    #вызов специфичной функции обработки для текущего сайта
    if 'text_func' in par:
        func = globals()[par['text_func']]
        text_tags = func(text_tags)
    if not text_tags:
        return None
    for i in text_tags.contents:
        if not i.name:
            continue
        #обработка абзацев
        if i.name == 'p':
            result.append(parse_paragraph(i))
        #обработка заголовков абзацев
        if re.match(r'^h\d',i.name):
            result.append('\n'.join([' ',i.text,' ']))
        #обработка цитат
        # if i.name == 'blockquote':
        #     if i.findAll('a'):
        #        result.append('{ %s }:{ %s }' % (i.p.text, i.findAll('a')[-1]['href']))
        #     else:
        #         result.append(i.text)
    return '\n'.join(result)

def btcnb_text(tag):
    #обработка текста статьи для bitcoinnewsbot
    text_tags = tag
    for tag in tag.contents:
        if tag.name == 'div':
            if not tag.attrs:
                text_tags = tag
            elif 'id' in tag.attrs and \
                  tag.attrs['id'].startswith('post-'):
                 tmp_tag = tag.find('div',{'class': 'entry-content'})
                 if tmp_tag:
                    text_tags = tmp_tag
                 else:
                    text_tags = tag
            elif 'itemprop' in tag.attrs and \
                 tag.attrs['itemprop'] == 'articleBody':
                 text_tags = tag
    return text_tags

def parse_paragraph(tag):
    #обработка абзаца
    result = []
    for tags in tag.contents:
        if tags.name == 'br':
            result.append('\n')
        #обработка гиперссылок
        elif tags.name == 'a':
            try:
                # result.append('{%s}:{%s}' % (tags.text,tags['href']))
                result.append('{%s}' % (tags.text))
            except KeyError:
                result.append(tags.text)
        elif hasattr(tags,'text'):
            result.append(tags.text)
        elif tags.name != 'img':
            result.append(tags.string.strip())
    return ' '.join(result)

def read_csv(par):
    #чтение csv и возврат обработанных ссылок
    file_name = par['csv_name']
    try:
        with open(file_name,'r',encoding='utf-8') as file:
            # reader = csv.reader(file,delimiter=',',quoting=csv.QUOTE_ALL)
            reader = csv.reader(file, delimiter='|', quoting=csv.QUOTE_ALL)
            if not reader:
                return None
            else:
                links = set()
                reader.__next__()
                for row in reader:
                    url = config.link_pattern.findall(row[3])#.strip("'"))
                    links.add(row[3])
                print(links)
                return links
    except FileNotFoundError:
        logging.error('CSV file not found %s' % file_name)

# def read_csv(par):
#     #чтение csv и возврат обработанных ссылок
#     file_name = par['csv_name']
#     try:
#         with open(file_name,'r',encoding='utf-8') as file:
#             # reader = csv.reader(file,delimiter=',',quoting=csv.QUOTE_ALL)
#             reader = csv.reader(file, delimiter='|', quoting=csv.QUOTE_ALL)
#             if not reader:
#                 return None
#             else:
#                 links = set()
#                 reader.__next__()
#                 for row in reader:
#                     url = config.link_pattern.findall(row[2].strip("'"))
#                     links.add(url[0])
#                 return links
#     except FileNotFoundError:
#         logging.error('CSV file not found %s' % file_name)

def write_csv(data,par,new=False):
    #запись результатов в csv
    file_name = par['csv_name']
    with open(file_name,'a',encoding='utf-8',newline='') as file:
        # writer = csv.writer(file,delimiter=',',quoting=csv.QUOTE_ALL)
        writer = csv.writer(file, delimiter='|', quotechar='"', quoting=csv.QUOTE_ALL)
        if new:
            logging.info('Create new csv file')
            writer.writerow(data)
            return
        for row in data:
            if not row:
                return
            if None in row:
                return
            else:
                writer.writerow(row)
        logging.info('%s new records in %s' % (len(data),file_name))

def start_parse(params):
    #запуск парсера
    par = config.params[params]
    if not os.path.exists(par['csv_name']):
        write_csv(['parse_date','title_date','author','url','views','shares','likes','title','text'],par,True)
    for url in par['urls']:
        resp = make_request(url)
        if resp:
            html = get_html(resp)
            get_links(html,read_csv(par),par)

if __name__ == '__main__':
    print('Scrapping module')