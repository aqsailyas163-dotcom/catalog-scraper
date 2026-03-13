"""Main entry point for the catalog scraper."""

import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper.crawler import CatalogCrawler
from scraper.parsers import ProductParser
from scraper.exporters import DataExporter
from scraper.utils import deduplicate_products


def main():
    """Run the complete scraping workflow."""
    print("="*60)
    print("E-Commerce Catalog Scraper")
    print("="*60)

    # Configuration
    BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"
    OUTPUT_DIR = "data"

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Initialize components
    crawler = CatalogCrawler(BASE_URL)
    parser = ProductParser(BASE_URL)
    exporter = DataExporter(OUTPUT_DIR)

    print(f"\nTarget website: {BASE_URL}")
    print(f"Output directory: {OUTPUT_DIR}\n")

    # Step 1: Discover categories
    print("\n" + "="*60)
    print("STEP 1: Discovering Categories")
    print("="*60)
    categories = crawler.discover_categories()
    print(f"\nFound {len(categories)} categories\n")

    # Step 2: Crawl all products
    print("\n" + "="*60)
    print("STEP 2: Crawling Products")
    print("="*60)
    all_product_links = []

    for category in categories:
        category_name = category['name']
        category_url = category['url']

        products = crawler.crawl_category_products(category_name, category_url)
        all_product_links.extend(products)

    print(f"\n{'='*60}")
    print(f"Total product links collected: {len(all_product_links)}")
    print("="*60)

    # Step 3: Parse product detail pages
    print("\n" + "="*60)
    print("STEP 3: Parsing Product Details")
    print("="*60)
    all_products = []

    for i, product_link in enumerate(all_product_links, 1):
        print(f"Parsing product {i}/{len(all_product_links)}: {product_link.get('title', 'Unknown')}")

        product_data = parser.parse_product_page(
            product_link['url'],
            product_link['category'],
            product_link['subcategory'],
            product_link['source_page']
        )

        if product_data:
            all_products.append(product_data)

    print(f"\nSuccessfully parsed {len(all_products)} products")

    # Step 4: Deduplicate products
    print("\n" + "="*60)
    print("STEP 4: Deduplicating Products")
    print("="*60)
    unique_products, duplicate_count = deduplicate_products(all_products)
    print(f"Removed {duplicate_count} duplicate products")
    print(f"Unique products: {len(unique_products)}")

    # Step 5: Export data
    print("\n" + "="*60)
    print("STEP 5: Exporting Data")
    print("="*60)
    exporter.export_products(unique_products, "products.csv")
    exporter.export_category_summary(unique_products, "category_summary.csv")
    exporter.update_summary_duplicates("category_summary.csv", duplicate_count)

    # Final summary
    print("\n" + "="*60)
    print("SCRAPING COMPLETED SUCCESSFULLY")
    print("="*60)
    print(f"Total products scraped: {len(unique_products)}")
    print(f"Duplicates removed: {duplicate_count}")
    print(f"Categories processed: {len(categories)}")
    print(f"\nOutput files:")
    print(f"  - {OUTPUT_DIR}/products.csv")
    print(f"  - {OUTPUT_DIR}/category_summary.csv")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
