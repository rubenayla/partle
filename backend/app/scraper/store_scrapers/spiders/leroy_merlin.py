import scrapy


class LeroyMerlinSpider(scrapy.Spider):
    name = "leroy_merlin"
    allowed_domains = ["leroymerlin.es"]
    start_urls = []

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.leroymerlin.es/productos/perfil-forma-cuadrada-de-acero-en-bruto-standers-alt-25-x-an-25mm-x-l-1-m-87825775.html",
            meta=dict(
                playwright=True,
                playwright_include_page=True,
            )
        )

    def parse(self, response):
        # Extract product name
        product_name = response.css('h1.product-header-title::text').get()
        if product_name:
            product_name = product_name.strip()

        # Extract price
        price = response.css('div.price-wrapper span.price::text').get()
        if price:
            price = price.strip().replace('.', '').replace(',', '.') # Remove thousand separators and replace comma with dot for decimal

        # Extract description (this might need refinement based on actual HTML)
        description = response.css('div.product-description p::text').get()
        if description:
            description = description.strip()

        yield {
            'product_name': product_name,
            'price': price,
            'description': description,
            'url': response.url,
        }
