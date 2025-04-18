import scrapy


class MonitorSpider(scrapy.Spider):
    name = "monitor"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = [
        "https://lista.mercadolivre.com.br/monitor-gamer?sb=rb#D[A:monitor%20gamer]"
    ]
    page_count = 1
    max_page = 10

    def parse(self, response):
        products = response.css(
            "ol.ui-search-layout.ui-search-layout--grid"
        ).css("li")

        for product in products:
            previous_price = (
                product.css(".andes-money-amount--previous")
                .css(".andes-money-amount__fraction::text")
                .get()
            )
            current_price = (
                product.css(".poly-price__current")
                .css(".andes-money-amount__fraction::text")
                .get()
            )

            yield {
                "brand": product.css(".poly-component__brand::text").get(),
                "title": product.css(".poly-component__title::text").get(),
                "seller": product.css(".poly-component__seller::text").get(),
                "review_rating": product.css(
                    ".poly-reviews__rating::text"
                ).get(),
                "review_total": product.css(
                    ".poly-reviews__total::text"
                ).get(),
                "old_price": previous_price,
                "new_price": current_price,
                "page": self.page_count,
            }

        if self.page_count < self.max_page:
            next_page_url = response.css(
                ".andes-pagination__button--next a::attr(href)"
            ).get()
            if next_page_url:
                self.page_count += 1
                yield scrapy.Request(url=next_page_url, callback=self.parse)
