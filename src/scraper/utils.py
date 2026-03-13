"""Utility functions for the scraper."""

import re
import time
from urllib.parse import urljoin
from typing import Optional
import requests
from bs4 import BeautifulSoup


def safe_request(url: str, max_retries: int = 3, delay: float = 1.0) -> Optional[requests.Response]:
    """
    Make a safe HTTP request with retry logic.

    Args:
        url: The URL to fetch
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds

    Returns:
        Response object if successful, None otherwise
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed for {url}: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
    return None


def join_url(base_url: str, relative_url: str) -> str:
    """
    Join a base URL with a relative URL.

    Args:
        base_url: The base URL
        relative_url: The relative URL to join

    Returns:
        The complete URL
    """
    return urljoin(base_url, relative_url)


def clean_text(text: Optional[str]) -> str:
    """
    Clean and normalize text by removing extra whitespace.

    Args:
        text: The text to clean

    Returns:
        Cleaned text
    """
    if text is None:
        return ""
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text.strip())
    return text


def parse_price(price_str: Optional[str]) -> Optional[float]:
    """
    Parse price string into a float value.

    Args:
        price_str: String containing price (e.g., "$123.45")

    Returns:
        Float value of price or None if parsing fails
    """
    if not price_str:
        return None

    try:
        # Remove currency symbols and commas, extract numbers
        price_str = clean_text(price_str)
        # Find all numbers including decimals
        match = re.search(r'[\d,]+\.?\d*', price_str.replace(',', ''))
        if match:
            return float(match.group())
    except (ValueError, AttributeError):
        pass

    return None


def parse_rating(rating_str: Optional[str]) -> Optional[int]:
    """
    Parse review count or rating string into an integer.

    Args:
        rating_str: String containing rating or review count

    Returns:
        Integer value or None if parsing fails
    """
    if not rating_str:
        return None

    try:
        # Extract numbers from string
        match = re.search(r'\d+', rating_str)
        if match:
            return int(match.group())
    except (ValueError, AttributeError):
        pass

    return None
