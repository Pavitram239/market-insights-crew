import yfinance as yf
from crewai.tools import tool

@tool("Live stock info tool")
def get_stock_price(stock_symbol: str) -> str:
    """
    Fetches the current stock price and other relevant information for the given stock symbol using yahoo finance.

    Parameters:
        stock_symbol (str): The ticker symbol of the stock (e.g., "AAPL" for Apple Inc).
    
    Returns:
        str: A summary of the current stock price and other relevant information.
    """

    stock = yf.Ticker(stock_symbol)
    info = stock.info

    current_price = info.get("regularMarketPrice")
    change = info.get("regularMarketChange")
    change_percent = info.get("regularMarketChangePercent")
    currency = info.get("currency", "USD")

    if current_price is None:
        return f"Could not retrieve data for stock symbol: {stock_symbol}"

    return (
        f"Stock: {stock_symbol.upper()}\n"
        f"Current Price: {current_price} {currency}\n"
        f"Change: {change} ({round(change_percent)}%)"
    )

# print(get_stock_price("AAPL"))