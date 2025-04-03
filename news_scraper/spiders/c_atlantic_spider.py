from datetime import datetime
import scrapy
import newspaper
from bs4 import BeautifulSoup


class CityNewsAtlanticSpider(scrapy.Spider):
    ''' City news scraper. - CityNews Atlantic @2025-03-27'''

    name = 'atlantic'
    category_url = 'https://halifax.citynews.ca/category/atlantic/'
    # set initial urls to scrape for this spider
    start_urls = [category_url]

    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    # ! dont rename this variable, it will break the pipeline!
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
        print('====== detected first article: CityNews - Atlantic ===============')
        yield response.follow(
            first_article_url, 
            self.parse_article, 
            cb_kwargs={'title': f"#1 {first_article_title}", 'index': 1}
        )

        # get other articles (except the first one)
        other_articles = latest_news_section.css(".card .card-body > a")
        print('====== detected other articles: ===============')
        print(len(other_articles))
        print('====================')
        for index, link_tag in enumerate(other_articles):
            other_article_url = link_tag.css("a::attr(href)").get()
            print(f"Article {index + 1}: {other_article_url}")
            other_article_title = link_tag.css("a::attr(title)").get()
            yield response.follow(
                other_article_url, 
                self.parse_article, 
                cb_kwargs={'title': f"#{index+1} {other_article_title}", 'index': index+1},
            )
        print('======== end of latest articles ============')

    def parse_article(self, response, title, index):
        # Use Newspaper4k to parse the article
        article = newspaper.Article(response.url, language='en')
        article.download(title=f"#{index} {title}", ignore_read_more=True)
        # remove unwanted tags
        soup = BeautifulSoup(article.html, 'html.parser')
        # ! remove page-component divs, it will break the parsing!
        for div in soup.find_all('div', class_=['page-component']):
            div.decompose()
        article.html = str(soup)
        article.parse()
        article.nlp()
        
        # Format publish date as string if it exists
        publish_date = None
        if article.publish_date:
            publish_date = article.publish_date.isoformat()
            
        # Create article data dictionary
        article_data = {
            'index': index,
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