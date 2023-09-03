from setuptools import setup, find_packages

setup(
    name='QuantEdgeMarketData',
    version='0.1.0',
    description='A Python package for fetching and managing historical market data using the Alpha Vantage API.',
    author='Your Name',
    author_email='your@email.com',
    url='https://github.com/yourusername/QuantEdgeMarketData',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
)