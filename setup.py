from setuptools import setup, find_packages

setup(
    name='binance-vision',
    version='1.0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'binance-vision = binance_vision.__main__:main',
        ],
    },
)
