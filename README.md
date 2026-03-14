# E-Commerce Catalog Scraper

A web scraping project for extracting product data from an e-commerce website.

## Project Description

This project scrapes product information from https://webscraper.io/test-sites/e-commerce/static. It navigates through categories, subcategories, and product pages to collect product details.

## Technologies Used

- Python 3.14
- uv (package manager)
- requests (for HTTP requests)
- BeautifulSoup4 (for HTML parsing)
- Git/GitHub (version control)

## Setup

1. Install uv package manager:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

## How to Run

```bash
uv run python main.py
```

The program will scrape the website and save results to the `data/` folder.

## Output Files

- `data/products.csv` - Contains all product details
- `data/category_summary.csv` - Contains category statistics
- `data/products.json` - JSON format of products
- `data/category_summary.json` - JSON format of summary

## Project Structure

```
├── main.py              # Main program
├── scraper/             # Scraper modules
│   ├── crawler.py       # For navigating website
│   ├── parsers.py       # For parsing product pages
│   ├── exporters.py     # For saving data
│   └── utils.py         # Helper functions
├── data/                # Output folder
└── pyproject.toml       # Project dependencies
```

## Git Branches

- `main` - Main branch
- `dev` - Development branch
- `feature/catalog-navigation` - Category discovery feature
- `feature/product-details` - Product parsing feature
- `fix/url-resolution` - URL handling fixes
- `fix/deduplication` - Duplicate removal fixes

## Features

- Discovers categories and subcategories automatically
- Handles pagination on listing pages
- Extracts product details from individual product pages
- Removes duplicate products
- Exports data to CSV and JSON formats

## Author

University of Central Punjab
Course: Tools & Technologies for Data Science
