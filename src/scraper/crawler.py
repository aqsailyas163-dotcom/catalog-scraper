"""Web crawler for discovering categories, subcategories, and products."""

from typing import List, Dict, Set
from bs4 import BeautifulSoup
from .utils import safe_request, join_url, clean_text


class CatalogCrawler:
    """Crawler for navigating the e-commerce catalog."""

    def __init__(self, base_url: str):
        """
        Initialize the crawler.

        Args:
            base_url: The base URL of the website
        """
        self.base_url = base_url
        self.visited_urls: Set[str] = set()

    def discover_categories(self) -> List[Dict[str, str]]:
        """
        Discover all categories from the main page.

        Returns:
            List of dictionaries with category name and URL
        """
        print(f"Discovering categories from {self.base_url}")
        response = safe_request(self.base_url)

        if not response:
            print("Failed to fetch main page")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        categories = []

        # Find category links in the navigation
        # The site uses a navbar with category links
        category_links = soup.select('a.category')

        for link in category_links:
            category_name = clean_text(link.get_text())
            category_url = join_url(self.base_url, link.get('href', ''))

            if category_name and category_url:
                categories.append({
                    'name': category_name,
                    'url': category_url
                })
                print(f"  Found category: {category_name}")

        return categories

    def discover_subcategories(self, category_url: str) -> List[Dict[str, str]]:
        """
        Discover all subcategories within a category.

        Args:
            category_url: URL of the category page

        Returns:
            List of dictionaries with subcategory name and URL
        """
        print(f"Discovering subcategories from {category_url}")
        response = safe_request(category_url)

        if not response:
            print("Failed to fetch category page")
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        subcategories = []

        # Find subcategory links (typically in sidebar or navigation)
        subcategory_links = soup.select('a.subcategory-link')

        for link in subcategory_links:
            subcategory_name = clean_text(link.get_text())
            subcategory_url = join_url(self.base_url, link.get('href', ''))

            if subcategory_name and subcategory_url:
                subcategories.append({
                    'name': subcategory_name,
                    'url': subcategory_url
                })
                print(f"    Found subcategory: {subcategory_name}")

        return subcategories

    def get_product_links_from_page(self, page_url: str, category: str, subcategory: str) -> List[Dict[str, str]]:
        """
        Extract all product links from a listing page.

        Args:
            page_url: URL of the listing page
            category: Category name
            subcategory: Subcategory name

        Returns:
            List of dictionaries with product URL and metadata
        """
        response = safe_request(page_url)

        if not response:
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        products = []

        # Find product cards/links
        product_cards = soup.select('.thumbnail')

        for card in product_cards:
            title_link = card.select_one('a.title')
            if title_link:
                product_url = join_url(self.base_url, title_link.get('href', ''))
                product_title = clean_text(title_link.get('title', ''))

                if product_url and product_url not in self.visited_urls:
                    products.append({
                        'url': product_url,
                        'title': product_title,
                        'category': category,
                        'subcategory': subcategory,
                        'source_page': page_url
                    })
                    self.visited_urls.add(product_url)

        return products

    def get_pagination_urls(self, page_url: str) -> List[str]:
        """
        Get all pagination URLs from a listing page.

        Args:
            page_url: URL of the current page

        Returns:
            List of pagination URLs
        """
        response = safe_request(page_url)

        if not response:
            return []

        soup = BeautifulSoup(response.content, 'html.parser')
        pagination_urls = []

        # Find pagination links
        pagination_links = soup.select('.pagination a')

        for link in pagination_links:
            href = link.get('href', '')
            if href:
                page_url_full = join_url(self.base_url, href)
                if page_url_full not in pagination_urls:
                    pagination_urls.append(page_url_full)

        return pagination_urls

    def crawl_category_products(self, category_name: str, category_url: str) -> List[Dict[str, str]]:
        """
        Crawl all products within a category including all subcategories and paginated pages.

        Args:
            category_name: Name of the category
            category_url: URL of the category

        Returns:
            List of product metadata dictionaries
        """
        print(f"\nCrawling category: {category_name}")
        all_products = []

        # Discover subcategories
        subcategories = self.discover_subcategories(category_url)

        # If no subcategories found, treat the category page as a listing page
        if not subcategories:
            print(f"  No subcategories found, treating as listing page")
            subcategories = [{'name': category_name, 'url': category_url}]

        for subcategory in subcategories:
            subcategory_name = subcategory['name']
            subcategory_url = subcategory['url']

            print(f"  Crawling subcategory: {subcategory_name}")

            # Get products from first page
            products = self.get_product_links_from_page(
                subcategory_url, category_name, subcategory_name
            )
            all_products.extend(products)
            print(f"    Found {len(products)} products on first page")

            # Get pagination URLs and crawl them
            pagination_urls = self.get_pagination_urls(subcategory_url)
            print(f"    Found {len(pagination_urls)} pagination URLs")

            for page_url in pagination_urls:
                if page_url != subcategory_url:  # Skip the first page
                    products = self.get_product_links_from_page(
                        page_url, category_name, subcategory_name
                    )
                    all_products.extend(products)
                    print(f"    Found {len(products)} products on {page_url}")

        print(f"Total products found in {category_name}: {len(all_products)}")
        return all_products
