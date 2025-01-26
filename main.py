import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_playwright.page import PageMethod

class CrisisWatchSpider(scrapy.Spider):
    """
    Spider to scrape crisis data from the Crisis Group website.
    """
    name = "crisisgroup"
    allowed_domains = ["crisisgroup.org"]
    country_ids = [93, 58, 1318, 8, 91]
    start_urls = [
        f"https://www.crisisgroup.org/crisiswatch/database?location[]={country_id}&created=-3+months" for country_id in country_ids
    ]

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": True,
        },
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Sec-Fetch-Site': 'same-origin',
        'Cookie': '_ga=GA1.2.1937342108.1737647916; _ga_0BDV0CNSW1=GS1.1.1737808763.4.1.1737808882.0.0.0; _gid=GA1.2.1679435514.1737808764',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Sec-Fetch-Mode': 'navigate',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15',
        'Referer': 'https://www.google.com/',
        'Priority': 'u=0, i',
    }

    def start_requests(self):
        """
        Generates initial requests to the start URLs.
        """
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                headers=self.headers,
                dont_filter=True,
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "//h1[contains(@class, 'c-page-hero__title')]")
                    ],
                    "playwright_page_goto_kwargs": {
                        "timeout": 60000,  # Timeout set to 60 seconds
                    },
                },
            )

    def parse(self, response):
        """
        Parses the response and extracts crisis data.
        """
        entries = response.xpath('//div[contains(@class, "c-crisiswatch-entry u-pr")]')

        for entry in entries:
            country_name = entry.xpath('normalize-space(.//h3[@class="u-df u-aic"]/span[contains(@class, "o-icon")]/following-sibling::text())').get()
            month_year = entry.xpath('normalize-space(.//time[contains(@class, "u-ttu u-fs13 u-fwn u-db u-gray--light u-mar-t10")]/text())').get()
            
            paragraphs = entry.xpath('.//div[contains(@class, "o-crisis-states__detail")]/p')
            title = paragraphs[0].xpath('normalize-space()').get() if paragraphs else ''
            paragraph = ' '.join(paragraph.xpath('normalize-space()').get() for paragraph in paragraphs[1:]).strip()

            yield {
                "country_name": country_name,
                "month_year": month_year,
                "title": title,
                "paragraph": paragraph,
            }

# Run the spider
if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "output.csv": {"format": "csv"},
            "output.json": {"format": "json", "encoding": "utf8", "ensure_ascii": False},
        },
    })
    process.crawl(CrisisWatchSpider)
    process.start()