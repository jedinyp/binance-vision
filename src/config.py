import os

class Config():
    BASE_URL = "https://data.binance.vision" # base path to Binance Vision
    OUTPUT_DIR = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        ), "output") # Folder where script dumps products
