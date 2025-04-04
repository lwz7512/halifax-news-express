import scrapy
import newspaper
from datetime import datetime


class GlobalNewsHalifaxSpider(scrapy.Spider):
    ''' Global News Halifax news scraper.'''

    name = 'global_news_halifax'
    category_url = 'https://globalnews.ca/halifax/'
    
    start_urls = [category_url]

    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    full_json_path = f'data/gn_halifax_{today_str}.json'
    
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
        latest_news_section = response.css("#home-topStories")

        # get the top-article link
        top_article_link = latest_news_section.css(".c-posts--gridMosaic li.c-posts__item a.c-posts__headlineLink")
        top_article_url = top_article_link.css("a::attr(href)").get()
        top_article_title = top_article_link.css("span::text").get()
        print('====== detected top article: Global News Halifax ===============')
        print(top_article_url)
        print(top_article_title)
        print('====================')
        yield response.follow(
            top_article_url, 
            self.parse_article, 
            cb_kwargs={'title': f"#1 {top_article_title}", 'index': 1}
        )
        
        latest_articles = latest_news_section.css(".c-posts--grid li.c-posts__item")
        print('====== detected latest articles: Global News Halifax ===============')
        print(len(latest_articles))
        print('====================')
        for index, li_tag in enumerate(latest_articles):
            link_title = li_tag.css("li::attr(data-caption)").get()
            link_url = li_tag.css("li > a::attr(href)").get()
            # the card could be `SPONSOR POST`, so need to skip it!
            if link_title == None or link_url == None:
                continue
            yield response.follow(
                link_url, 
                self.parse_article, 
                cb_kwargs={'title': f"#{index+1} {link_title}", 'index': index + 1}
            )
        print('======== end of latest articles ============')

    def parse_article(self, response, title, index):
        # Use Newspaper4k to parse the article
        article = newspaper.Article(response.url, language='en')
        article.download(input_html=response.text, title=title, ignore_read_more=True)
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