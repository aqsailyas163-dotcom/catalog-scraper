# Teaching Guide: E-Commerce Catalog Scraper Project

## Overview for Students

This document will help you understand the complete web scraping project, from concept to implementation.

---

## Table of Contents

1. [Project Goal](#project-goal)
2. [Architecture Overview](#architecture-overview)
3. [Git Branching Strategy](#git-branching-strategy)
4. [Code Structure Walkthrough](#code-structure-walkthrough)
5. [How Each Module Works](#how-each-module-works)
6. [Workflow Explanation](#workflow-explanation)
7. [Key Concepts](#key-concepts)
8. [Common Questions](#common-questions)

---

## Project Goal

### What are we building?
A **web scraper** that automatically extracts product information from an e-commerce website.

### Why?
In real-world scenarios, you might need to:
- Collect product prices for price comparison
- Monitor competitors
- Gather data for analysis
- Create product catalogs

### Target Website
`https://webscraper.io/test-sites/e-commerce/static`

This is a practice website designed for learning web scraping.

---

## Architecture Overview

### The Big Picture

```
┌─────────────────────────────────────────────────────────┐
│                    MAIN.PY                              │
│                 (Orchestrator)                          │
└────────────┬────────────────────────────────────────────┘
             │
             ├──────► CatalogCrawler ──► Discovers categories
             │        (crawler.py)     ├► Finds subcategories
             │                         ├► Handles pagination
             │                         └► Collects product URLs
             │
             ├──────► ProductParser ───► Visits product pages
             │        (parsers.py)     └► Extracts product data
             │
             ├──────► Utils ───────────► URL joining
             │        (utils.py)       ├► Text cleaning
             │                         ├► Price parsing
             │                         └► Deduplication
             │
             └──────► DataExporter ────► Exports products.csv
                      (exporters.py)   └► Exports category_summary.csv
```

### File Structure

```
catalog-scraper/
│
├── main.py                  # Entry point - runs everything
│
├── scraper/                 # Main package
│   ├── __init__.py         # Makes it a Python package
│   ├── crawler.py          # Navigates the website
│   ├── parsers.py          # Extracts data from pages
│   ├── exporters.py        # Saves data to CSV
│   └── utils.py            # Helper functions
│
├── data/                    # Output folder
│   ├── products.csv        # All products
│   └── category_summary.csv # Statistics
│
├── pyproject.toml          # uv configuration
└── README.md               # Documentation
```

---

## Git Branching Strategy

### Why Multiple Branches?

In professional development, we don't write all code on `main` because:
- **Isolation**: Each feature is developed separately
- **Safety**: Main branch stays stable
- **Collaboration**: Multiple people can work simultaneously
- **Review**: Changes can be reviewed before merging

### Our Branch Strategy

```
main (Production - Always Working)
 │
 ├─── dev (Development - Integration)
 │     │
 │     ├─── feature/catalog-navigation (New Feature 1)
 │     │     └── Implement category discovery
 │     │
 │     ├─── feature/product-details (New Feature 2)
 │     │     └── Implement product parsing
 │     │
 │     ├─── fix/url-resolution (Bug Fix 1)
 │     │     └── Improve URL handling
 │     │
 │     └─── fix/deduplication (Bug Fix 2)
 │           └── Remove duplicate products
 │
 └─── After testing, merge dev → main
```

### Workflow Steps (Show on Git Graph)

```bash
# Step 1: Initialize
git init
git add .
git commit -m "Initial project setup"

# Step 2: Create dev branch
git checkout -b dev

# Step 3: Create feature branch
git checkout -b feature/catalog-navigation

# Step 4: Work on feature
# ... make changes ...
git commit -m "feat: implement catalog navigation"

# Step 5: Merge to dev
git checkout dev
git merge feature/catalog-navigation

# Step 6: Repeat for other features
# Step 7: Finally merge dev to main
git checkout main
git merge dev
```

---

## Code Structure Walkthrough

### 1. Main.py - The Orchestrator

**Purpose**: Controls the entire scraping workflow

```python
def main():
    # Step 1: Setup
    crawler = CatalogCrawler(BASE_URL)
    parser = ProductParser(BASE_URL)
    exporter = DataExporter(OUTPUT_DIR)

    # Step 2: Discover categories
    categories = crawler.discover_categories()

    # Step 3: Crawl all products
    for category in categories:
        products = crawler.crawl_category_products(...)

    # Step 4: Parse product details
    for product_link in all_product_links:
        product_data = parser.parse_product_page(...)

    # Step 5: Deduplicate
    unique_products = deduplicate_products(all_products)

    # Step 6: Export
    exporter.export_products(unique_products)
    exporter.export_category_summary(unique_products)
```

**Teaching Points**:
- This is the "controller" - it calls other modules
- It follows a clear step-by-step process
- Easy to understand the flow

---

### 2. crawler.py - The Navigator

**Purpose**: Navigate through the website structure

#### Key Method: `discover_categories()`

```python
def discover_categories(self):
    # 1. Fetch the main page
    response = safe_request(self.base_url)

    # 2. Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # 3. Find category links
    category_links = soup.select('a.category-link')

    # 4. Extract name and URL
    for link in category_links:
        category_name = clean_text(link.get_text())
        category_url = join_url(self.base_url, link.get('href'))
```

**Teaching Points**:
- Uses CSS selectors (`a.category-link`) to find elements
- `BeautifulSoup` parses HTML into a searchable structure
- Returns a list of dictionaries with category info

#### Key Method: `get_pagination_urls()`

```python
def get_pagination_urls(self, page_url):
    # Find all pagination links like "2", "3", "Next"
    pagination_links = soup.select('.pagination a')

    # Extract unique URLs
    for link in pagination_links:
        page_url_full = join_url(self.base_url, link.get('href'))
```

**Teaching Points**:
- E-commerce sites split products across multiple pages
- We need to visit ALL pages to get ALL products
- This method finds those page links

---

### 3. parsers.py - The Data Extractor

**Purpose**: Extract specific data from product pages

#### Key Method: `parse_product_page()`

```python
def parse_product_page(self, product_url, ...):
    # 1. Fetch the product page
    response = safe_request(product_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 2. Extract title
    title_elem = soup.select_one('.title')
    title = clean_text(title_elem.get_text())

    # 3. Extract price
    price_elem = soup.select_one('.price')
    price = parse_price(price_elem.get_text())

    # 4. Extract description
    description_elem = soup.select_one('.description')
    description = clean_text(description_elem.get_text())

    # 5. Return as dictionary
    return {
        'title': title,
        'price': price,
        'description': description,
        ...
    }
```

**Teaching Points**:
- Each product page has structured HTML
- We use CSS selectors to find specific elements
- Data is cleaned and normalized before returning

---

### 4. utils.py - The Helper Functions

**Purpose**: Provide reusable utility functions

#### Key Function: `join_url()`

```python
def join_url(base_url, relative_url):
    # Handles:
    # base: "https://example.com"
    # relative: "/product/1"
    # result: "https://example.com/product/1"

    return urljoin(base_url, relative_url)
```

**Why Needed?**
- HTML often contains relative URLs like `/product/1`
- We need full URLs like `https://example.com/product/1`
- `urljoin` handles all edge cases

#### Key Function: `parse_price()`

```python
def parse_price(price_str):
    # Input: "$1,234.56"
    # Output: 1234.56

    # Remove currency symbols and commas
    # Extract numeric value
    # Convert to float

    return float(match.group())
```

**Why Needed?**
- Prices appear as text: "$1,234.56"
- We need numbers for calculations: 1234.56
- This function handles various formats

#### Key Function: `deduplicate_products()`

```python
def deduplicate_products(products):
    seen_urls = set()
    unique_products = []

    for product in products:
        url = normalize_url(product['product_url'])

        if url not in seen_urls:
            seen_urls.add(url)
            unique_products.append(product)

    return unique_products, duplicate_count
```

**Why Needed?**
- Same product might appear multiple times
- URLs might differ slightly: `HTTP` vs `http`, trailing `/`
- We normalize and track seen URLs

---

### 5. exporters.py - The Data Saver

**Purpose**: Export data to CSV files

#### Key Method: `export_products()`

```python
def export_products(self, products, filename):
    # Define columns
    fieldnames = ['category', 'subcategory', 'title', 'price', ...]

    # Write CSV
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for product in products:
            writer.writerow(product)
```

**Teaching Points**:
- CSV = Comma-Separated Values (Excel-compatible)
- Each product becomes one row
- Headers define column names

#### Key Method: `export_category_summary()`

```python
def export_category_summary(self, products):
    # Group products by subcategory
    # Calculate statistics:
    #   - Total products
    #   - Average price
    #   - Min/Max price
    #   - Missing descriptions

    # Export to CSV
```

**Teaching Points**:
- Aggregates data for analysis
- Shows summary statistics per category
- Useful for business insights

---

## Workflow Explanation

### Step-by-Step Execution

#### **Step 1: Discover Categories**

```
User runs: uv run python main.py

main.py calls: crawler.discover_categories()

Crawler:
  1. Fetches https://webscraper.io/test-sites/e-commerce/static
  2. Finds links with class "category-link"
  3. Returns: [
       {'name': 'Computers', 'url': '...'},
       {'name': 'Phones', 'url': '...'}
     ]
```

**Output**:
```
Discovering categories from https://...
  Found category: Computers
  Found category: Phones
Found 2 categories
```

---

#### **Step 2: Discover Subcategories**

```
For each category:
  Crawler calls: discover_subcategories(category_url)

For "Computers":
  1. Fetches https://.../computers
  2. Finds links with class "subcategory-link"
  3. Returns: [
       {'name': 'Laptops', 'url': '...'},
       {'name': 'Tablets', 'url': '...'}
     ]
```

---

#### **Step 3: Handle Pagination**

```
For "Laptops":
  1. Visit page 1: https://.../computers/laptops
  2. Find pagination links
  3. Get URLs for pages 2, 3, 4, ... 20

  For each page:
    - Extract product links
    - Store product URLs
```

**Why Important?**
- Page 1 might have only 6 products
- But there are 20 pages total
- We need ALL products, not just first page

---

#### **Step 4: Extract Product Details**

```
For each product URL:
  1. Visit product page
  2. Extract:
     - Title: "Lenovo ThinkPad"
     - Price: $1,311.99
     - Description: "15.6 inch, Core i5..."
     - Image URL: https://.../image.png
     - Reviews: 12 reviews
  3. Store in list
```

**Example Product Page**:
```html
<h4 class="title">Lenovo ThinkPad</h4>
<h4 class="price">$1,311.99</h4>
<p class="description">15.6 inch laptop...</p>
```

Becomes:
```python
{
    'title': 'Lenovo ThinkPad',
    'price': 1311.99,
    'description': '15.6 inch laptop...',
    ...
}
```

---

#### **Step 5: Deduplicate**

```
Before: 120 products (with duplicates)
After:  118 products (2 duplicates removed)

How?
  - Normalize URLs (lowercase, remove trailing /)
  - Track seen URLs in a set
  - Keep only first occurrence
```

---

#### **Step 6: Export**

```
Creates two files:

1. products.csv (all products)
   category,subcategory,title,price,url,...
   Computers,Laptops,ThinkPad,1311.99,...
   Computers,Laptops,ProBook,739.99,...
   ...

2. category_summary.csv (statistics)
   subcategory,total_products,avg_price,min_price,max_price
   Computers > Laptops,118,756.16,306.99,1311.99
   ...
```

---

## Key Concepts

### 1. Web Scraping Basics

**What is Web Scraping?**
- Automatically extracting data from websites
- Like copying data, but automated

**How it Works**:
1. **HTTP Request**: Ask server for webpage
2. **HTML Response**: Server sends HTML code
3. **Parse HTML**: Convert HTML to searchable structure
4. **Extract Data**: Find specific elements (title, price, etc.)
5. **Store Data**: Save to CSV, database, etc.

**Visual Example**:
```
Browser View:          HTML Code:
┌─────────────┐       <div class="product">
│ Laptop      │         <h4 class="title">Laptop</h4>
│ $999.99     │         <span class="price">$999.99</span>
└─────────────┘       </div>

Our Scraper:
soup.select_one('.title')  → "Laptop"
soup.select_one('.price')  → "$999.99"
```

---

### 2. CSS Selectors

**What are CSS Selectors?**
- A way to find HTML elements
- Like "find all elements with class 'title'"

**Common Selectors**:
```python
# Class selector
soup.select('.title')           # All elements with class="title"

# ID selector
soup.select('#main-title')      # Element with id="main-title"

# Tag selector
soup.select('h1')               # All <h1> elements

# Combined selector
soup.select('div.product')      # <div> with class="product"

# Descendant selector
soup.select('.product .title')  # .title inside .product
```

**Example**:
```html
<div class="product">
  <h4 class="title">Laptop</h4>
  <span class="price">$999</span>
</div>
```

```python
soup.select('.product')       # Returns the <div>
soup.select('.title')         # Returns <h4>
soup.select('.price')         # Returns <span>
```

---

### 3. URL Handling

**Absolute vs Relative URLs**:

```python
# Absolute URL (complete)
"https://example.com/product/1"

# Relative URL (missing domain)
"/product/1"                    # Needs base URL
"../product/1"                  # Go up one level
"product/1"                     # Relative to current path
```

**join_url() in Action**:
```python
base = "https://example.com/catalog"
relative = "/product/1"

join_url(base, relative)
# Result: "https://example.com/product/1"
```

**Why Important?**
- HTML links are often relative
- We need full URLs to make requests
- `join_url` handles all edge cases

---

### 4. Data Cleaning

**Why Clean Data?**

Raw scraped data is messy:
```
Price: "$1,234.56   "  (spaces, symbols)
Title: "Laptop\n\n  "  (newlines, spaces)
URL: "HTTPS://Example.COM/path/"  (inconsistent)
```

Clean data:
```
Price: 1234.56         (float)
Title: "Laptop"        (trimmed)
URL: "https://example.com/path"  (normalized)
```

**Cleaning Functions**:
```python
clean_text("  Hello\n\n")       → "Hello"
parse_price("$1,234.56")        → 1234.56
normalize_url("HTTPS://Ex.COM/") → "https://ex.com"
```

---

### 5. Error Handling

**Why Needed?**
- Websites might be down
- HTML structure might change
- Network issues

**Example**:
```python
try:
    response = requests.get(url)
    response.raise_for_status()
    return response
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    return None
```

**Safe Extraction**:
```python
# Bad (might crash)
title = soup.select_one('.title').get_text()

# Good (handles missing elements)
title_elem = soup.select_one('.title')
title = clean_text(title_elem.get_text()) if title_elem else ""
```

---

## Common Questions

### Q1: Why use uv instead of pip?

**Answer**:
- **Modern**: Latest Python package manager
- **Fast**: Faster than pip
- **Better dependency resolution**: Handles conflicts better
- **Project management**: Creates virtual environments automatically

```bash
# Old way (pip)
python -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4

# New way (uv)
uv sync  # Done! Creates venv and installs everything
```

---

### Q2: Why Beautiful Soup and not Selenium?

**Answer**:

| Feature | Beautiful Soup | Selenium |
|---------|---------------|----------|
| Speed | ⚡ Fast | 🐢 Slow |
| Use Case | Static HTML | JavaScript-heavy |
| Browser | ❌ No | ✅ Yes |
| Resource | 💾 Light | 🏋️ Heavy |

**Our website** is static HTML → Beautiful Soup is perfect!

---

### Q3: What if the website changes?

**Answer**:
Update the CSS selectors!

```python
# Old selector (stopped working)
category_links = soup.select('a.category')

# New selector (website changed class name)
category_links = soup.select('a.category-link')
```

**How to find new selectors?**
1. Open website in browser
2. Right-click element → "Inspect"
3. See HTML structure
4. Update selector in code

---

### Q4: How do we handle pagination?

**Answer**:
```python
# 1. Get first page
products = get_products_from_page(url)

# 2. Find pagination links
pagination_urls = get_pagination_urls(url)

# 3. Visit each page
for page_url in pagination_urls:
    more_products = get_products_from_page(page_url)
    products.extend(more_products)
```

**Example**:
```
Page 1: https://example.com/laptops        (6 products)
Page 2: https://example.com/laptops?page=2 (6 products)
Page 3: https://example.com/laptops?page=3 (6 products)
...
Total: 118 products across 20 pages
```

---

### Q5: Why deduplicate products?

**Answer**:
Same product might appear in:
- Multiple categories
- Multiple pages (pagination overlap)
- Similar URLs (http vs https, with/without /)

**Solution**:
```python
# Normalize URLs
"https://example.com/product/1/" → "https://example.com/product/1"
"HTTP://EXAMPLE.COM/product/1"  → "https://example.com/product/1"

# Track seen URLs
if url not in seen_urls:
    seen_urls.add(url)
    keep_product()
else:
    skip_duplicate()
```

---

## Teaching Tips

### Demo Flow (Live Demonstration)

#### 1. **Show the Website** (5 min)
- Open https://webscraper.io/test-sites/e-commerce/static
- Navigate: Home → Computers → Laptops → Product
- Show pagination (Page 1, 2, 3...)
- Right-click → Inspect to show HTML

#### 2. **Show Git Branches** (5 min)
```bash
# List branches
git branch -a

# Show branch graph
git log --graph --oneline --all

# Checkout different branches
git checkout feature/catalog-navigation
git checkout main
```

#### 3. **Walk Through Code** (20 min)
- Open `main.py` → explain workflow
- Open `crawler.py` → show category discovery
- Open `parsers.py` → show data extraction
- Open `utils.py` → show helper functions

#### 4. **Run the Scraper** (10 min)
```bash
# Run with visible output
uv run python main.py
```
- Show progress messages
- Show created CSV files
- Open CSVs in Excel/Numbers

#### 5. **Test Components** (10 min)
```bash
# Test category discovery
uv run python -c "from scraper.crawler import CatalogCrawler; c = CatalogCrawler('https://...'); print(c.discover_categories())"

# Test product parsing
# (Show individual component testing)
```

---

### Assessment Questions

**Basic Understanding**:
1. What is web scraping?
2. What does BeautifulSoup do?
3. Why do we need pagination handling?
4. What is the difference between `main` and `dev` branches?

**Intermediate**:
1. Explain how CSS selectors work
2. Why do we normalize URLs?
3. What is the purpose of deduplication?
4. Walk through the scraping workflow

**Advanced**:
1. How would you modify this to scrape a different website?
2. What would break if the website changes its HTML structure?
3. How would you add rate limiting to avoid overwhelming the server?
4. Explain the Git workflow and why each branch exists

---

### Hands-On Exercises

**Exercise 1: Modify Selectors**
- Task: Update CSS selectors for a different class name
- Learning: Understanding HTML structure

**Exercise 2: Add a New Field**
- Task: Extract product ratings (if available)
- Learning: Extending the parser

**Exercise 3: Create a New Branch**
- Task: Create `feature/add-ratings` branch
- Learning: Git workflow

**Exercise 4: Export to JSON**
- Task: Add JSON export functionality
- Learning: Data formats

---

## Summary

### What Students Should Learn

1. **Web Scraping Fundamentals**
   - How websites are structured (HTML)
   - How to extract data programmatically
   - Handling pagination and navigation

2. **Software Engineering Practices**
   - Modular code organization
   - Git branching workflow
   - Error handling
   - Documentation

3. **Python Skills**
   - Working with libraries (requests, BeautifulSoup)
   - File I/O (CSV export)
   - Data structures (lists, dictionaries, sets)
   - String manipulation and parsing

4. **Tools**
   - uv package manager
   - Git version control
   - GitHub collaboration
   - Command line usage

---

## Next Steps

After mastering this project, students can:

1. **Extend the scraper**
   - Add more data fields
   - Scrape images (download them)
   - Add database storage

2. **Scrape other websites**
   - News sites
   - Job boards
   - Product comparisons

3. **Add features**
   - Email notifications
   - Price tracking
   - Scheduled scraping (cron jobs)

4. **Learn advanced topics**
   - Asynchronous scraping (faster)
   - Handling JavaScript sites (Selenium)
   - Anti-scraping techniques (proxies, headers)

---

## Resources for Students

- **BeautifulSoup Documentation**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **Requests Documentation**: https://requests.readthedocs.io/
- **Git Branching Tutorial**: https://learngitbranching.js.org/
- **CSS Selectors Reference**: https://www.w3schools.com/cssref/css_selectors.php
- **uv Documentation**: https://docs.astral.sh/uv/

---

**End of Teaching Guide**

Good luck with your teaching! This project covers many important concepts in a practical, real-world scenario.
