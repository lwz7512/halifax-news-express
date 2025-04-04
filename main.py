
from scrapy.crawler import CrawlerProcess
from twisted.internet import defer

from news_scraper.spiders.a_gove_spider import GovernmentSpider
from news_scraper.spiders.a_econ_spider import EconomySpider
from news_scraper.spiders.c_local_spider import CityNewsLocalSpider
from news_scraper.spiders.c_atlantic_spider import CityNewsAtlanticSpider
from news_scraper.spiders.g_halifax_spider import GlobalNewsHalifaxSpider

from convertor import convert_json_to_markdown


# if article nlp method got error, run this codes once:
# import nltk
# nltk.download('punkt')


def crawl_concurrently():
    process = CrawlerProcess()
    # First spider
    process.crawl(GovernmentSpider)
    # Second spider
    process.crawl(EconomySpider)
    # Third spider
    process.crawl(CityNewsLocalSpider)
    # Fourth spider
    process.crawl(CityNewsAtlanticSpider)
    # Fifth spider
    process.crawl(GlobalNewsHalifaxSpider)
    # start all spiders
    process.start()


def main():
    print(">>> running spiders concurrently...")
    # crawl_concurrently()
    print("### all spiders finished!")
    print(">>> converting JSON files to Markdown...")
    # then convert the json files to markdown
    convert_json_to_markdown()
    print("### conversion completed!")


if __name__ == "__main__":
    print(">>> starting main...")
    main()
    print("### main finished!")
