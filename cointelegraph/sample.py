import bitparser
import config

# общий код
# try:
# 	for i in config.params.keys():
# 		bitparser.parser_thread(i).start()
# except:
# 	print('Thread error')

# код для historical data cointelegraph постатейного парсинга
for art in config.params['cointelegraph']['urls_art']:
    result = bitparser.parse_article(art, config.params['cointelegraph'], True)
    print(result, type(result))
    bitparser.write_csv([result], config.params['cointelegraph'])

# рабочий код
# art = bitparser.parse_article(
# 	"https://cointelegraph.com/news/bitcoin-will-not-become-legal-in-india-without-monitoring-says-chief-economist",
# 	config.params['cointelegraph'], True)
# print(art,type(art))
# bitparser.write_csv([art],config.params['cointelegraph'])

# рабочий код тестовый. без циклов
# art = bitparser.parse_article(
#     "https://cointelegraph.com/news/bitcoin-will-not-become-legal-in-india-without-monitoring-says-chief-economist",
#     config.params['cointelegraph'], True)
# art1 = bitparser.parse_article(
#     "https://cointelegraph.com/news/bitcoin-beats-classic-cars-art-wines-in-luxury-investment-index",
#     config.params['cointelegraph'], True)
# print(art, type(art))
# print(art1, type(art1))
# bitparser.write_csv([art, art1], config.params['cointelegraph'])

