from src.misc import generate_date_list
from src.config import Config
import requests
import zipfile
import os

def build_urls(symbol: str, market: str, data: str, date_range: tuple[str, str], resolution: str = "1m") -> list[tuple[str, str]]:
    """
    Generates Binance urls based on chosen parameters.
    Args:
        symbol (str): The symbol to fetch data for.
        market (str): The market to fetch data for.
        data (str): The type of data to fetch.
        data_range (tuple[str, str]): The date range to fetch data for.
    Returns:
        None
    """

    match market:
        case "spot":
            url_part = f"{Config.BASE_URL}/data/spot/daily/{data}/{symbol}/{resolution}/{symbol}-{resolution}"
        case "futures-um":
            url_part = f"{Config.BASE_URL}/data/futures/um/daily/{data}/{symbol}/{resolution}/{symbol}-{resolution}"
        case "futures-cm":
            url_part = f"{Config.BASE_URL}/data/futures/cm/daily/{data}/{symbol}/{resolution}/{symbol}-{resolution}"
        case "options":
            url_part = f"{Config.BASE_URL}/data/option/daily/{data}/{symbol}/{symbol}-{data}"
        case _:
            raise ValueError(f"Invalid market: {market}")

    # Generate url for each date in range
    dates = generate_date_list(date_range)
    output = []
    for date in dates:
        output.append((url_part + f"-{date}.zip", 
                       f"{symbol}-{market}-{data}-{resolution}-{date}"))
    return output

def fetch_products(query: dict, output_folder = Config.OUTPUT_DIR) -> None:
    """
    Fetches file from url and saves it to output_folder.
    Args:
        url_list (list[str]): List of urls to fetch.
        output_folder (str): Folder to save files to.
    Returns:
        None
    """

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through urls and skip already downloaded files
    for url, file_name in query:

        # Check for both zip and csv variants
        partial_path = os.path.join(output_folder, file_name)
        if os.path.exists(partial_path + ".zip"):
            print(f"File already exists: {partial_path + ".zip"}")
            continue
        elif os.path.exists(partial_path + ".csv"):
            print(f"File already exists: {partial_path + ".csv"}")
            continue

        # Download url and save zip file to output folder
        response = requests.get(url)
        if response.status_code == 200:
            output_path = os.path.join(output_folder, file_name + ".zip")
            with open(output_path, "wb") as f:
                f.write(response.content)
                print(f"File saved to {output_path}")
        else:
            raise Warning(f"Failed to fetch {url}")
        
    return None

import os
import zipfile

def unzip_products(output_folder=Config.OUTPUT_DIR) -> None:
    """
    Unzips all .zip files in output_folder.
    If a zip contains one CSV, renames it to match the zip file name.
    Args:
        output_folder (str): Folder to search for zip files.
    Returns:
        None
    """
    for file in os.listdir(output_folder):
        if file.endswith(".zip"):
            try:
                zip_path = os.path.join(output_folder, file)
                base_name = os.path.splitext(file)[0]  

                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(output_folder)
                    extracted_files = zip_ref.namelist()

                # find CSV file inside
                csv_files = [f for f in extracted_files if f.lower().endswith(".csv")]
                if len(csv_files) == 1:
                    old_csv_path = os.path.join(output_folder, csv_files[0])
                    new_csv_path = os.path.join(output_folder, f"{base_name}.csv")

                    # handle subfolders in zip
                    if os.path.dirname(csv_files[0]):
                        old_csv_path = os.path.join(output_folder, os.path.basename(csv_files[0]))
                    os.rename(old_csv_path, new_csv_path)
                os.remove(zip_path)
                print(f"Unzipped and renamed {file}")
            except FileExistsError:
                print(f"File already exists {file}")
            except Exception as e:
                print(f"Error unzipping {file}: {e}")

    return None
