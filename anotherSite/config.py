import re

# заголовки запроса, прикидываемся браузером
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}

"""словарь с параметрами парсинга для каждого сайта

ключ словаря (например ctlgrph)- идентефикатор для парсинга конкретного сайта

browse_url - адрес сайта, для сравнения ссылок и выполнения запросов
urls - массив ссылок для просмотра ссылок на статьи
link_to_art - словарь с параметрами тэгов для извлечения ссылок
	tag - тэг
	attr - аттрибут тэга
	attr_value - значение аттрибута тэга
title - словарь с параметрами тэгa для извлечения заголовка
	tag - тэг
	attr - аттрибут тэга
	attr_value - значение аттрибута тэга
body - словарь с параметрами тэгa для извлечения заголовка
	tag - тэг
	attr - аттрибут тэга
	attr_value - значение аттрибута тэга
csv_name - имя файла для сохранение результатов
short_link - True, если ссылки извлекаются без полного адреса

text_func - необязательный ключ, название функции для
	извлечения текста с особыми или неоднородными параметрами.
	Например для http://bitnewsbot.com/
"""

params = {'coindesk':
           {'browse_url': 'https://news.bitcoin.com',
			'urls': [
                'https://news.bitcoin.com/page/2/',
                'https://news.bitcoin.com/page/3/',
            ],


			'links_to_art': {'tag': 'h3', 'attr': 'class', 'attr_value': re.compile(r'^post-')},
			'title': {'tag': 'h3', 'attr': 'class', 'attr_value': 'article-top-title'},
			'author': {'tag': 'a', 'attr': 'class', 'attr_value': 'article-container-lab-name'},
			# 'date_time': {'tag': 'time', 'attr': 'datetime', 'attr_value': re.compile(r'^.*$')},
			'date_time': {'tag': 'meta', 'attr': 'property', 'attr_value': 'article:published_time'},
			'views': {'tag': 'div', 'attr': 'class', 'attr_value': 'referral_stats total-views'}, # Views: (int)
			'shares': {'tag': 'span', 'attr': 'class', 'attr_value': 'count'},  # Shares: (int)
			'likes': {'tag': 'div', 'attr': 'class', 'attr_value': 'likes'},  # Likes: (int)
			'body': {'tag': 'div', 'attr': 'class', 'attr_value': 'article-content-container'},
			'short_link': False,
			'csv_name': 'coindesk.csv'
				}
		  }

link_pattern = re.compile(r'^http.*\.\w*/(.*)')

# re.compile(r'^post-')