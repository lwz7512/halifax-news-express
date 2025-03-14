import scrapy
import newspaper
from datetime import datetime


class EconomySpider(scrapy.Spider):
    ''' Economy news scraper. - Halifax Examiner'''

    name = 'economy'
    category_url = 'https://www.halifaxexaminer.ca/category/economy/'
    
    start_urls = [category_url]

    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    full_json_path = f'data/he_economy_{today_str}.json'
    
    custom_settings = {
        'LOG_LEVEL': 'WARNING',
        'FEEDS': {
            full_json_path: {
                'format': 'json',
                'encoding': 'utf8',
                'indent': 2,
                'overwrite': True
            }
        }
    }

    def parse(self, response):
        # Extract URLs from the response and yield Scrapy Requests
        latest_news_section = response.css(".wp-block-newspack-blocks-homepage-articles")
        latest_articles = latest_news_section.css("article .entry-title > a::attr(href)")
        print('====== detected latest articles: ===============')
        print(len(latest_articles))
        print('====================')
        for href in latest_articles:
            print(href)
            yield response.follow(href, self.parse_article)
        print('======== end of latest articles ============')

    def parse_article(self, response):
        # Use Newspaper4k to parse the article
        article = newspaper.Article(response.url, language='en')
        article.download(input_html=response.text)
        article.parse()
        article.nlp()
        
        # Format publish date as string if it exists
        publish_date = None
        if article.publish_date:
            publish_date = article.publish_date.isoformat()
            
        # Create article data dictionary
        article_data = {
            'title': article.title,
            'authors': article.authors,
            'url': response.url,
            # 'text': article.text,
            'publish_date': publish_date,
            'keywords': article.keywords,
            'summary': article.summary,
            'scraped_at': datetime.now().isoformat()
        }
        
        yield article_data