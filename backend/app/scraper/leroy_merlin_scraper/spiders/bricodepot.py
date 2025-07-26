import scrapy


class BricodepotSpider(scrapy.Spider):
    name = "bricodepot"
    allowed_domains = ["bricodepot.es"]
    def start_requests(self):
        yield scrapy.Request(
            url="https://www.bricodepot.es/",
            callback=self.parse,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_goto_kwargs={
                    'wait_until': 'domcontentloaded',
                    'timeout': 60000,
                },
                playwright_page_methods=[
                    {'method': 'wait_for_selector', 'args': ['body']},
                ],
            ),
            dont_filter=True,
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        html_content = await page.content()
        await page.close()
        response = response.replace(body=html_content, encoding='utf-8')

        # Extract category links from the homepage
        category_links = response.css('a.hm-link.main-navbar--item-parent::attr(href)').getall()
        for link in category_links:
            yield scrapy.Request(
                url=response.urljoin(link),
                callback=self.parse_category,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_goto_kwargs={
                        'wait_until': 'domcontentloaded',
                        'timeout': 60000,
                    },
                    playwright_page_methods=[
                        {'method': 'wait_for_selector', 'args': ['body']},
                    ],
                ),
                dont_filter=True,
            )

    async def parse_category(self, response):
        page = response.meta["playwright_page"]
        html_content = await page.content()
        await page.close()
        response = response.replace(body=html_content, encoding='utf-8')

        # Extract product links from the category page
        product_links = response.css('a.product-item-link::attr(href)').getall()
        for link in product_links:
            yield scrapy.Request(
                url=response.urljoin(link),
                callback=self.parse_product,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_goto_kwargs={
                        'wait_until': 'domcontentloaded',
                        'timeout': 60000,
                    },
                    playwright_page_methods=[
                        {'method': 'wait_for_selector', 'args': ['body']},
                    ],
                ),
                dont_filter=True,
            )

    async def parse_product(self, response):
        page = response.meta["playwright_page"]
        html_content = await page.content()
        await page.close()
        response = response.replace(body=html_content, encoding='utf-8')

        # Extract product name
        product_name = response.css('h1.product-name::text').get()
        if product_name:
            product_name = product_name.strip()

        # Extract price
        price = response.css('span.price::text').get()
        if price:
            price = price.strip().replace('.', '').replace(',', '.')

        # Extract description (this might need refinement based on actual HTML)
        description = response.css('div.product-description-content p::text').get()
        if description:
            description = description.strip()

        yield {
            'product_name': product_name,
            'price': price,
            'description': description,
            'url': response.url,
        }
