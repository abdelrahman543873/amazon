import scrapy
from scrapy.loader import ItemLoader
from ..items import AmazonItem
import re
from scrapy.selector import Selector


class QuoteSpider(scrapy.Spider):
    name = "phones"
    start_urls = [
        "https://www.amazon.com/s?i=computers-intl-ship&page=2"]

    def parse(self, response):
        products_links = response.xpath(
            "//span[@class='a-size-base-plus a-color-base a-text-normal']/ancestor::a/@href").getall()
        products_images = response.xpath(
            "//div[@class='a-section a-spacing-medium']/span/a/div/img/@src").getall()
        products_titles = response.css(
            ".a-color-base.a-text-normal::text").getall()
        products_ratings = response.css(
            ".aok-align-bottom > span.a-icon-alt::text").getall()
        products_no_reviews = response.xpath(
            "//span[@class='a-size-base']/text()").getall()
        for product in range(len(products_links)):
            result = products_links[product].find('dp/') + 3
            second = products_links[product].find('/ref')
            feature = "https://www.amazon.com/hz/reviews-render/ajax/lazy-widgets/stream?asin=" + products_links[
                product][
                result:second] + "&lazyWidget=cr-summarization-attributes"
            products_links[product] = "https://www.amazon.com" + \
                products_links[product]
            request = scrapy.Request(
                url=str(feature), callback=self.properties)
            request.cb_kwargs['image_urls'] = products_images[product]
            request.cb_kwargs['link'] = products_links[product]
            request.cb_kwargs['title'] = products_titles[product]
            request.cb_kwargs['rating'] = products_ratings[product]
            request.cb_kwargs['no_of_reviews'] = products_no_reviews[product]
            yield request
        next_page = response.xpath(
            "//ul[@class='a-pagination']/li[last()]/a/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def properties(self, response, image_urls, link, title, rating, no_of_reviews):
        filtering = response.text.replace("\\", "")
        advs = Selector(text=filtering).css(
            "span.a-size-base.a-color-base").css("::text").getall()
        classifications = Selector(text=filtering).css(
            "span.a-size-base.a-color-tertiary").css("::text").getall()
        final = ''
        for (adv, classification) in zip(advs, classifications):
            final += '\n' + adv + "   " + classification
        request = scrapy.Request(url=link, callback=self.product_page)
        request.cb_kwargs['image_urls'] = image_urls
        request.cb_kwargs['link'] = link
        request.cb_kwargs['title'] = title
        request.cb_kwargs['rating'] = rating
        request.cb_kwargs['no_of_reviews'] = no_of_reviews
        request.cb_kwargs['features'] = final
        yield request

    def product_page(self, response, image_urls, link, title, rating, no_of_reviews, features):
        comments = response.xpath(
            "//div[@data-hook='review-collapsed']/span[ not(@*) or @class='cr-original-review-content']").getall()
        reviewers_names = response.xpath(
            "//span[@class='a-profile-name']/text()").getall()
        customers_ratings = response.xpath(
            "//i[@data-hook='review-star-rating' or @data-hook='cmps-review-star-rating']/span[@class='a-icon-alt']/text()").getall()
        final = ''
        for (comment, reviewers_name, customers_rating) in zip(comments, reviewers_names, customers_ratings):
            final += '\n' + reviewers_name + '\n' + customers_rating + \
                '\n' + re.sub('<.*?>', '', comment, flags=re.DOTALL) + '\n'
        description = ''.join(response.xpath(
            "//span[@class='a-list-item']//text()").getall()).strip().replace('\t', '').replace('\n', '')
        comments = final
        rating_distribution = response.xpath(
            "//span[@class='a-size-base']/a[@class='a-link-normal']/@title").getall()
        # this here is used to load the items in the loader and then in the pipeline each item is loaded in the database using sqlalcemy
        loader = ItemLoader(item=AmazonItem())
        loader.add_value('image_urls', image_urls)
        loader.add_value('link', link)
        loader.add_value('title', title)
        loader.add_value('rating', rating)
        loader.add_value('no_of_reviews', no_of_reviews)
        loader.add_value('description', description)
        loader.add_value('comments', comments)
        loader.add_value('rating_distribution', ' '.join(rating_distribution))
        loader.add_value('features', features)
        yield loader.load_item()
