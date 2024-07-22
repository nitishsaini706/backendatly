# scraper.py
from bs4 import BeautifulSoup
from typing import List, Optional
import httpx
from models import Product  # Assuming Product is a Pydantic model or similar
from utils import retry

class Scraper:
    def __init__(self, limit: Optional[int] = None, proxy: Optional[str] = None):
        self.base_url = "https://dentalstall.com/shop/"
        self.limit = limit
        self.proxy = proxy

    @retry
    async def scrape_page(self, page: int) -> List[Product]:
        url = f"{self.base_url}?page={page}"
        async with httpx.AsyncClient(proxies=self.proxy) as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            soup = BeautifulSoup(response.text, "html.parser")
            products = self.parse_products(soup)
            return products

    def parse_products(self, soup: BeautifulSoup) -> List[Product]:
        products = []
        product_elements = soup.select('li.product')  

        for product in product_elements:
            title_element = product.select_one('.woo-loop-product__title a')
            price_element = product.select_one('.price ins .woocommerce-Price-amount')
            image_element = product.select_one('.mf-product-thumbnail img')

            if title_element and price_element and image_element:
                title = title_element.get_text(strip=True)
                price = float(price_element.get_text(strip=True).replace('₹', '').replace(',', ''))
                image_url = image_element['src']

                product_instance = Product(
                    product_title=title,
                    product_price=price,
                    path_to_image=image_url
                )
                products.append(product_instance)

        return products

    async def scrape(self) -> List[Product]:
        products = []
        page = 1
        while True:
            if self.limit and page > self.limit:
                break
            
            page_products = await self.scrape_page(page)
            if not page_products:
                break
            
            products.extend(page_products)
            page += 1
        
        return products
