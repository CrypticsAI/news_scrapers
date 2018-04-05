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

params = {'bitcoinmagazine':
              {'browse_url': 'https://bitcoinmagazine.com/',
		       'urls': [
                   # 'https://bitcoinmagazine.com/articles/',
		   			'https://bitcoinmagazine.com/articles/?page=1',
                    'https://bitcoinmagazine.com/articles/?page=2',
                    'https://bitcoinmagazine.com/articles/?page=3',
                    # 'https://bitcoinmagazine.com/articles/?page=4',
                    # 'https://bitcoinmagazine.com/articles/?page=5',
                    # 'https://bitcoinmagazine.com/articles/?page=6',
                    # 'https://bitcoinmagazine.com/articles/?page=7',
                    # 'https://bitcoinmagazine.com/articles/?page=8',
                    # 'https://bitcoinmagazine.com/articles/?page=9',
                    # 'https://bitcoinmagazine.com/articles/?page=10',
                    # 'https://bitcoinmagazine.com/articles/?page=11',
                    # 'https://bitcoinmagazine.com/articles/?page=12',
                    # 'https://bitcoinmagazine.com/articles/?page=13',
                    # 'https://bitcoinmagazine.com/articles/?page=14',
                    # 'https://bitcoinmagazine.com/articles/?page=15',
                    # 'https://bitcoinmagazine.com/articles/?page=16',
                    # 'https://bitcoinmagazine.com/articles/?page=17',
                    # 'https://bitcoinmagazine.com/articles/?page=18',
                    # 'https://bitcoinmagazine.com/articles/?page=19',
                    # 'https://bitcoinmagazine.com/articles/?page=20',
                    # 'https://bitcoinmagazine.com/articles/?page=21',
                    # 'https://bitcoinmagazine.com/articles/?page=22',
                    # 'https://bitcoinmagazine.com/articles/?page=23',
                    # 'https://bitcoinmagazine.com/articles/?page=24',
                    # 'https://bitcoinmagazine.com/articles/?page=25',
                    # 'https://bitcoinmagazine.com/articles/?page=26',
                    # 'https://bitcoinmagazine.com/articles/?page=27',
                    # 'https://bitcoinmagazine.com/articles/?page=28',
                    # 'https://bitcoinmagazine.com/articles/?page=29',
                    # 'https://bitcoinmagazine.com/articles/?page=30',
                    # 'https://bitcoinmagazine.com/articles/?page=31',
                    # 'https://bitcoinmagazine.com/articles/?page=32',
                    # 'https://bitcoinmagazine.com/articles/?page=33',
                    # 'https://bitcoinmagazine.com/articles/?page=34',
                    # 'https://bitcoinmagazine.com/articles/?page=35',
                    # 'https://bitcoinmagazine.com/articles/?page=36',
                    # 'https://bitcoinmagazine.com/articles/?page=37',
                    # 'https://bitcoinmagazine.com/articles/?page=38',
                    # 'https://bitcoinmagazine.com/articles/?page=39',
                    # 'https://bitcoinmagazine.com/articles/?page=40',
                    # 'https://bitcoinmagazine.com/articles/?page=41',
                    # 'https://bitcoinmagazine.com/articles/?page=42',
                    # 'https://bitcoinmagazine.com/articles/?page=43',
                    # 'https://bitcoinmagazine.com/articles/?page=44',
                    # 'https://bitcoinmagazine.com/articles/?page=45',
                    # 'https://bitcoinmagazine.com/articles/?page=46',
                    # 'https://bitcoinmagazine.com/articles/?page=47',
                    # 'https://bitcoinmagazine.com/articles/?page=48',
                    # 'https://bitcoinmagazine.com/articles/?page=49',
                    # 'https://bitcoinmagazine.com/articles/?page=50',
                    # 'https://bitcoinmagazine.com/articles/?page=51',
                    # 'https://bitcoinmagazine.com/articles/?page=52',
                    # 'https://bitcoinmagazine.com/articles/?page=53',
                    # 'https://bitcoinmagazine.com/articles/?page=54',
                    # 'https://bitcoinmagazine.com/articles/?page=55',
                    # 'https://bitcoinmagazine.com/articles/?page=56',
                    # 'https://bitcoinmagazine.com/articles/?page=57',
                    # 'https://bitcoinmagazine.com/articles/?page=58',
                    # 'https://bitcoinmagazine.com/articles/?page=59',
                    # 'https://bitcoinmagazine.com/articles/?page=60',
                    # 'https://bitcoinmagazine.com/articles/?page=61',
                    # 'https://bitcoinmagazine.com/articles/?page=62',
                    # 'https://bitcoinmagazine.com/articles/?page=63',
                    # 'https://bitcoinmagazine.com/articles/?page=64',
                    # 'https://bitcoinmagazine.com/articles/?page=65',
                    # 'https://bitcoinmagazine.com/articles/?page=66',
                    # 'https://bitcoinmagazine.com/articles/?page=67',
                    # 'https://bitcoinmagazine.com/articles/?page=68',
                    # 'https://bitcoinmagazine.com/articles/?page=69',
                    # 'https://bitcoinmagazine.com/articles/?page=70',
                    # 'https://bitcoinmagazine.com/articles/?page=71',
                    # 'https://bitcoinmagazine.com/articles/?page=72',
                    # 'https://bitcoinmagazine.com/articles/?page=73',
                    # 'https://bitcoinmagazine.com/articles/?page=74',
                    # 'https://bitcoinmagazine.com/articles/?page=75',
                    # 'https://bitcoinmagazine.com/articles/?page=76',
                    # 'https://bitcoinmagazine.com/articles/?page=77',
                    # 'https://bitcoinmagazine.com/articles/?page=78',
                    # 'https://bitcoinmagazine.com/articles/?page=79',
                    # 'https://bitcoinmagazine.com/articles/?page=80',
                    # 'https://bitcoinmagazine.com/articles/?page=81',
                    # 'https://bitcoinmagazine.com/articles/?page=82',
                    # 'https://bitcoinmagazine.com/articles/?page=83',
                    # 'https://bitcoinmagazine.com/articles/?page=84',
                    # 'https://bitcoinmagazine.com/articles/?page=85',
                    # 'https://bitcoinmagazine.com/articles/?page=86',
                    # 'https://bitcoinmagazine.com/articles/?page=87',
                    # 'https://bitcoinmagazine.com/articles/?page=88',
                    # 'https://bitcoinmagazine.com/articles/?page=89',
                    # 'https://bitcoinmagazine.com/articles/?page=90',
                    # 'https://bitcoinmagazine.com/articles/?page=91',
                    # 'https://bitcoinmagazine.com/articles/?page=92',
                    # 'https://bitcoinmagazine.com/articles/?page=93',
                    # 'https://bitcoinmagazine.com/articles/?page=94',
                    # 'https://bitcoinmagazine.com/articles/?page=95',
                    # 'https://bitcoinmagazine.com/articles/?page=96',
                    # 'https://bitcoinmagazine.com/articles/?page=97',
                    # 'https://bitcoinmagazine.com/articles/?page=98',
                    # 'https://bitcoinmagazine.com/articles/?page=99',
                    # 'https://bitcoinmagazine.com/articles/?page=100',
                    # 'https://bitcoinmagazine.com/articles/?page=101',
                    # 'https://bitcoinmagazine.com/articles/?page=102',
                    # 'https://bitcoinmagazine.com/articles/?page=103',
                    # 'https://bitcoinmagazine.com/articles/?page=104',
                    # 'https://bitcoinmagazine.com/articles/?page=105',
                    # 'https://bitcoinmagazine.com/articles/?page=106',
                    # 'https://bitcoinmagazine.com/articles/?page=107',
                    # 'https://bitcoinmagazine.com/articles/?page=108',
                    # 'https://bitcoinmagazine.com/articles/?page=109',
                    # 'https://bitcoinmagazine.com/articles/?page=110',
                    # 'https://bitcoinmagazine.com/articles/?page=111',
                    # 'https://bitcoinmagazine.com/articles/?page=112',
                    # 'https://bitcoinmagazine.com/articles/?page=113',
                    # 'https://bitcoinmagazine.com/articles/?page=114',
                    # 'https://bitcoinmagazine.com/articles/?page=115',
                    # 'https://bitcoinmagazine.com/articles/?page=116',
                    # 'https://bitcoinmagazine.com/articles/?page=117',
                    # 'https://bitcoinmagazine.com/articles/?page=118',
                    # 'https://bitcoinmagazine.com/articles/?page=119',
                    # 'https://bitcoinmagazine.com/articles/?page=120',
                    # 'https://bitcoinmagazine.com/articles/?page=121',
                    # 'https://bitcoinmagazine.com/articles/?page=122',
                    # 'https://bitcoinmagazine.com/articles/?page=123',
                    # 'https://bitcoinmagazine.com/articles/?page=124',
                    # 'https://bitcoinmagazine.com/articles/?page=125',
                    # 'https://bitcoinmagazine.com/articles/?page=126',
                    # 'https://bitcoinmagazine.com/articles/?page=127',
                    # 'https://bitcoinmagazine.com/articles/?page=128',
                    # 'https://bitcoinmagazine.com/articles/?page=129',
                    # 'https://bitcoinmagazine.com/articles/?page=130',
                    # 'https://bitcoinmagazine.com/articles/?page=131',
                    # 'https://bitcoinmagazine.com/articles/?page=132',
                    # 'https://bitcoinmagazine.com/articles/?page=133',
                    # 'https://bitcoinmagazine.com/articles/?page=134',
                    # 'https://bitcoinmagazine.com/articles/?page=135',
                    # 'https://bitcoinmagazine.com/articles/?page=136',
                    # 'https://bitcoinmagazine.com/articles/?page=137',
                    # 'https://bitcoinmagazine.com/articles/?page=138',
                    # 'https://bitcoinmagazine.com/articles/?page=139',
                    # 'https://bitcoinmagazine.com/articles/?page=140',
                    # 'https://bitcoinmagazine.com/articles/?page=141',
                    # 'https://bitcoinmagazine.com/articles/?page=142',
                    # 'https://bitcoinmagazine.com/articles/?page=143',
                    # 'https://bitcoinmagazine.com/articles/?page=144',
                    # 'https://bitcoinmagazine.com/articles/?page=145',
                    # 'https://bitcoinmagazine.com/articles/?page=146',
                    # 'https://bitcoinmagazine.com/articles/?page=147',
                    # 'https://bitcoinmagazine.com/articles/?page=148',
                    # 'https://bitcoinmagazine.com/articles/?page=149',
                    # 'https://bitcoinmagazine.com/articles/?page=150'
                    # 'https://bitcoinmagazine.com/articles/?page=151'
                    # 'https://bitcoinmagazine.com/articles/?page=152'
		   			],
                'links_to_art': {'tag':'div','attr': 'class','attr_value': 'col-lg-11'},
                'title': {'tag': 'meta','attr': 'property','attr_value': 'og:title'},
				'author': {'tag': 'meta', 'attr': 'name', 'attr_value': 'author'},
                'date_time': {'tag': 'time', 'attr': 'class', 'attr_value': 'article--time'},
				'views': {'tag': 'div', 'attr': 'class', 'attr_value': 'referral_stats total-views'}, # Views: (int)
				'shares': {'tag': 'span', 'attr': 'class', 'attr_value': 'count'},  # Shares: (int)
				'likes': {'tag': 'div', 'attr': 'class', 'attr_value': 'likes'},  # Likes: (int)
                'body' : {'tag': 'div','attr': 'class', 'attr_value': 'rich-text'},
                'short_link': True,
                'csv_name': 'bitcoinmagazine.csv'
                        }
               }
		  
link_pattern = re.compile(r'^http.*\.\w*/(.*)')

# re.compile(r'^post-')