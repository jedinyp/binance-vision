from src.core import build_urls, fetch_products, unzip_products
from src.loader import load_products

# Example usage
if __name__ == "__main__":

    # Parameters
    symbol = "BTCBVOLUSDT"
    market = "options"
    data = "BVOLIndex"
    resolution = "1m"
    date_range = ("2025-09-01", "2025-09-04")
    
    # Download and extract data
    urls = build_urls(symbol, market, data, date_range, resolution)
    fetch_products(urls)
    unzip_products()
    in_memory = load_products(symbol, market, data, date_range, resolution)
    
    print(in_memory)