"""Export scraped data to CSV files."""

import csv
from typing import List, Dict
from collections import defaultdict


class DataExporter:
    """Export product data and summaries to CSV files."""

    def __init__(self, output_dir: str = "data"):
        """
        Initialize the exporter.

        Args:
            output_dir: Directory to save CSV files
        """
        self.output_dir = output_dir

    def export_products(self, products: List[Dict], filename: str = "products.csv") -> None:
        """
        Export products to a CSV file.

        Args:
            products: List of product dictionaries
            filename: Name of the output CSV file
        """
        if not products:
            print("No products to export")
            return

        filepath = f"{self.output_dir}/{filename}"

        # Define CSV columns
        fieldnames = [
            'category',
            'subcategory',
            'title',
            'price',
            'product_url',
            'image_url',
            'description',
            'review_count',
            'details',
            'source_page'
        ]

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for product in products:
                    # Ensure all fields exist
                    row = {field: product.get(field, '') for field in fieldnames}
                    writer.writerow(row)

            print(f"Exported {len(products)} products to {filepath}")

        except Exception as e:
            print(f"Error exporting products: {e}")

    def export_category_summary(self, products: List[Dict], filename: str = "category_summary.csv") -> None:
        """
        Generate and export category summary statistics.

        Args:
            products: List of product dictionaries
            filename: Name of the output CSV file
        """
        if not products:
            print("No products to summarize")
            return

        filepath = f"{self.output_dir}/{filename}"

        # Group products by subcategory
        subcategory_data = defaultdict(list)

        for product in products:
            category = product.get('category', 'Unknown')
            subcategory = product.get('subcategory', 'Unknown')
            key = f"{category} > {subcategory}"
            subcategory_data[key].append(product)

        # Calculate statistics
        summary_rows = []

        for subcategory_key, prods in subcategory_data.items():
            # Extract prices
            prices = [p.get('price') for p in prods if p.get('price') is not None]

            # Count missing descriptions
            missing_descriptions = sum(1 for p in prods if not p.get('description', '').strip())

            # Calculate stats
            total_products = len(prods)
            avg_price = sum(prices) / len(prices) if prices else 0
            min_price = min(prices) if prices else 0
            max_price = max(prices) if prices else 0

            summary_rows.append({
                'subcategory': subcategory_key,
                'total_products': total_products,
                'average_price': round(avg_price, 2),
                'min_price': min_price,
                'max_price': max_price,
                'missing_descriptions': missing_descriptions,
                'duplicates_removed': 0  # Will be set by the caller
            })

        # Sort by subcategory name
        summary_rows.sort(key=lambda x: x['subcategory'])

        # Write to CSV
        fieldnames = [
            'subcategory',
            'total_products',
            'average_price',
            'min_price',
            'max_price',
            'missing_descriptions',
            'duplicates_removed'
        ]

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(summary_rows)

            print(f"Exported category summary to {filepath}")

        except Exception as e:
            print(f"Error exporting summary: {e}")

    def update_summary_duplicates(self, filename: str, duplicate_count: int) -> None:
        """
        Update the summary CSV with the total duplicate count.

        Args:
            filename: Name of the summary CSV file
            duplicate_count: Total number of duplicates removed
        """
        filepath = f"{self.output_dir}/{filename}"

        try:
            # Read existing data
            with open(filepath, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)

            # Update first row with duplicate count (as a global stat)
            if rows:
                rows[0]['duplicates_removed'] = duplicate_count

            # Write back
            fieldnames = list(rows[0].keys()) if rows else []
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

        except Exception as e:
            print(f"Error updating summary duplicates: {e}")
