import datetime

def get_current_time():
    """Returns the current local time."""
    return datetime.datetime.now().strftime("%I:%M %p")

def calculate_investment_growth(principal: float, rate: float, years: int):
    """Calculates simple interest growth."""
    amount = principal * (1 + (rate/100) * years)
    return f"${amount:,.2f}"

AVAILABLE_TOOLS = {
    "get_current_time": get_current_time,
    "calculate_investment_growth": calculate_investment_growth
}
