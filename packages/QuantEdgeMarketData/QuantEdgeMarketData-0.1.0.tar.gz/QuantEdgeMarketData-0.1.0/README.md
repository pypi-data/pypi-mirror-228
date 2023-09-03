# QuantEdgeMarketData

QuantEdgeMarketData is a Python package for fetching and managing historical market data using the Alpha Vantage API.

## Features
- Load historical daily price data for a given stock ticker.
- Filter data by date range.
- Retrieve data as a Pandas DataFrame.

## Installation

You can install QuantEdgeMarketData using pip:

```bash
pip install QuantEdgeMarketData
```

**Usage**
```python
import QuantEdgeMarketData as qemd

# Set your Alpha Vantage API key (replace 'YourApiKey' with your actual API key)
qemd.set_api_key('YourApiKey')

# Load historical price data for AAPL stock from 2022-01-01 to 2022-12-31
data = qemd.load_historical_data(stock_ticker="AAPL", start_date="2022-01-01", end_date="2022-12-31")

# Print the first few rows of the data
print(data.head())
```

**Documentation**
For detailed documentation and usage examples, please visit the [QuantEdgeMarketData Documentation](http://127.0.0.1:5000/backtesting).


**License**
This project is licensed under the MIT License - see the [LICENSE](http://127.0.0.1:5000/backtesting) file for details.


