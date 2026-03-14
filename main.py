"""
E-Commerce Web Scraper
Main program that scrapes product data from the website.
"""

import os
from scraper.crawler import SimpleCrawler
from scraper.parsers import SimpleParser
from scraper.exporters import SimpleExporter
from scraper.utils import remove_duplicates


def main():
    """
    Main function - Runs the complete scraping process.
    Steps: Find categories -> Get products -> Parse details -> Save to files
    """
    print("="*60)
    print("  E-COMMERCE WEB SCRAPER")
    print("="*60)
    print()

    # Configuration
    WEBSITE = "https://webscraper.io/test-sites/e-commerce/static"
    OUTPUT_FOLDER = "data"

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Initialize scraper components
    print("Setting up scraper...")
    crawler = SimpleCrawler(WEBSITE)
    parser = SimpleParser(WEBSITE)
    exporter = SimpleExporter(OUTPUT_FOLDER)
    print("✓ Ready!\n")

    # ========== STEP 2: FIND CATEGORIES ==========
    print("="*60)
    print("STEP 1: Finding Categories")
    print("="*60)
    categories = crawler.find_categories()
    print(f"\n✓ Found {len(categories)} categories\n")

    # ========== STEP 3: COLLECT PRODUCT URLs ==========
    print("="*60)
    print("STEP 2: Collecting Product URLs")
    print("="*60)

    all_product_links = []

    # Go through each category
    for category in categories:
        category_name = category['name']
        category_url = category['url']

        # Get all products in this category
        products = crawler.get_all_products_in_category(category_name, category_url)
        all_product_links.extend(products)

    print(f"\n✓ Total product links found: {len(all_product_links)}\n")

    # ========== STEP 4: GET PRODUCT DETAILS ==========
    print("="*60)
    print("STEP 3: Getting Product Details")
    print("="*60)

    all_products = []
    total = len(all_product_links)

    # Visit each product page
    for i, product_link in enumerate(all_product_links, 1):
        print(f"[{i}/{total}] {product_link['title'][:40]}...")

        # Extract all product information
        product_data = parser.get_product_details(
            product_link['url'],
            product_link['category'],
            product_link['subcategory'],
            product_link['source_page']
        )

        if product_data:
            all_products.append(product_data)

    print(f"\n✓ Extracted details for {len(all_products)} products\n")

    # ========== STEP 5: REMOVE DUPLICATES ==========
    print("="*60)
    print("STEP 4: Removing Duplicates")
    print("="*60)

    unique_products, dup_count = remove_duplicates(all_products)
    print(f"✓ Removed {dup_count} duplicate products")
    print(f"✓ Final count: {len(unique_products)} unique products\n")

    # ========== STEP 6: SAVE TO FILES ==========
    print("="*60)
    print("STEP 5: Saving Data")
    print("="*60)

    # Save as CSV (Excel format)
    exporter.save_to_csv(unique_products, "products.csv")
    exporter.save_summary_csv(unique_products, "category_summary.csv")

    # Save as JSON (Web format)
    exporter.save_to_json(unique_products, "products.json")
    exporter.save_summary_json(unique_products, "category_summary.json")

    # ========== DONE! ==========
    print()
    print("="*60)
    print("  SCRAPING COMPLETE!")
    print("="*60)
    print(f"Total Products: {len(unique_products)}")
    print(f"Duplicates Removed: {dup_count}")
    print(f"Categories: {len(categories)}")
    print()
    print("Output Files:")
    print(f"  📄 {OUTPUT_FOLDER}/products.csv")
    print(f"  📄 {OUTPUT_FOLDER}/products.json")
    print(f"  📄 {OUTPUT_FOLDER}/category_summary.csv")
    print(f"  📄 {OUTPUT_FOLDER}/category_summary.json")
    print("="*60)


# Run the program when this file is executed
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Stopped by user")
    except Exception as error:
        print(f"\n\n❌ Error: {error}")
        print("Please check your internet connection and try again.")
