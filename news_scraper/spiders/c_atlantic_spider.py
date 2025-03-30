import scrapy
import newspaper
from datetime import datetime


class CityNewsAtlanticSpider(scrapy.Spider):
    ''' City news scraper. - CityNews Atlantic @2025-03-27'''

    name = 'atlantic'
    category_url = 'https://halifax.citynews.ca/category/atlantic/'
    
    start_urls = [category_url]

    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    full_json_path = f'data/cn_atlantic_{today_str}.json'
    
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
        latest_news_section = response.css(".archive-more-articles")

        # get the first-article card
        first_article_card = latest_news_section.css(".first-article .card .card-body > a")
        first_article_url = first_article_card.css("a::attr(href)").get()
        first_article_title = first_article_card.css("a::attr(title)").get()
        print('====== detected first article: CityNews Atlantic ===============')
        yield response.follow(first_article_url, self.parse_article, cb_kwargs={'title': first_article_title})

        # get other articles (except the first one)
        other_articles = latest_news_section.css(".card .card-body > a")
        print('====== detected other articles: ===============')
        print(len(other_articles))
        print('====================')
        for link_tag in other_articles:
            other_article_url = link_tag.css("a::attr(href)").get()
            print(other_article_url)
            other_article_title = link_tag.css("a::attr(title)").get()
            yield response.follow(other_article_url, self.parse_article, cb_kwargs={'title': other_article_title})
        print('======== end of latest articles ============')

    def parse_article(self, response, title):
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
            'title': title,
            'authors': article.authors,
            'url': response.url,
            # 'text': article.text,
            'publish_date': publish_date,
            'keywords': article.keywords,
            'summary': article.summary,
            'scraped_at': datetime.now().isoformat()
        }
        
        yield article_data