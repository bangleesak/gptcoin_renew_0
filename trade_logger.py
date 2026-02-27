# trade_logger.py

trade_history = []

def log_trade(action, price, amount):
    trade = {"action": action, "price": price, "amount": amount}
    trade_history.append(trade)

def calculate_profit():
    profit = 0.0
    buy_price = None
    buy_amount = None

    for trade in trade_history:
        if trade["action"] == "buy":
            buy_price = trade["price"]
            buy_amount = trade["amount"]
        elif trade["action"] == "sell" and buy_price is not None:
            matched_amount = min(buy_amount, trade["amount"])
            profit += (trade["price"] - buy_price) * matched_amount
            buy_price = None

    return profit

def calculate_profit_rate():
    total_spent = 0.0
    total_earned = 0.0
    holding_btc = 0.0
    avg_buy_price = 0.0

    for trade in trade_history:
        if trade["action"] == "buy":
            total_spent += trade["price"] * trade["amount"]
            holding_btc += trade["amount"]
        elif trade["action"] == "sell":
            total_earned += trade["price"] * trade["amount"]
            holding_btc -= trade["amount"]

    net = total_earned - total_spent
    if total_spent == 0:
        return 0.0
    return (net / total_spent) * 100

def count_trades():
    buys = sum(1 for t in trade_history if t["action"] == "buy")
    sells = sum(1 for t in trade_history if t["action"] == "sell")
    return buys, sells

def average_buy_price():
    total_amount = 0.0
    total_spent = 0.0
    for trade in trade_history:
        if trade["action"] == "buy":
            total_spent += trade["price"] * trade["amount"]
            total_amount += trade["amount"]
    if total_amount == 0:
        return 0.0
    return total_spent / total_amount
