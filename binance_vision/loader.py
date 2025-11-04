import pandas as pd
import os
from .misc import generate_date_list
from .config import Config

def load_products(symbol: str, market: str, data: str, date_range: tuple[str, str], resolution: str = "1m", output_folder = Config.OUTPUT_DIR):
    """
    Loads downloaded csv data into memory.
    Args:
        symbol (str): The symbol to fetch data for.
        market (str): The market to fetch data for.
        data (str): The type of data to fetch.
        data_range (tuple[str, str]): The date range to fetch data for.
    Returns:
        None
    """

    dates = generate_date_list(date_range)
    df_list = []

    # Reenact filepath generation logic to load them
    for date in dates:
        try:
            file_name = f"{symbol}-{market}-{data}-{resolution}-{date}.csv"
            output_path = os.path.join(output_folder, file_name)
            df = pd.read_csv(output_path)
            print(f"Loaded {output_path}")
            df_list.append(df)
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {symbol}-{market}-{data}-{resolution}-{date}.csv")
        
    return pd.concat(df_list)