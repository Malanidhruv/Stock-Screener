def print_stocks(stocks):
    """Prints the stocks that gained 3-5%."""
    print("\nStocks that were 3-5% up yesterday:")
    print(f"{'Name':<20} {'Token':<10} {'Close':<10} {'Change (%)':<10}")
    print('-' * 50)
    for stock in stocks:
        print(f"{stock['Name']:<20} {stock['Token']:<10} {stock['Close']:<10.2f} {stock['Change (%)']:<10.2f}")
    print('-' * 50)
