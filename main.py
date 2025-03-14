
from scrapy.crawler import CrawlerProcess
from twisted.internet import defer

from news_scraper.spiders.a_gove_spider import GovernmentSpider
from news_scraper.spiders.a_econ_spider import EconomySpider

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
    process.start()


def main():
    print(">>> running spiders concurrently...")
    crawl_concurrently()
    print(">>> all spiders finished!")
    print(">>> converting JSON files to Markdown...")
    convert_json_to_markdown()
    print(">>> conversion completed!")


if __name__ == "__main__":
    print(">>> starting main...")
    main()
    print(">>> main finished!")
