from display_utils import display_portfolio, display_adjustments
from constants import PRICES_AND_UNITS, TARGET_WEIGHTS


def compute_percentages(client_portfolio):
    total_value = sum(client_portfolio.values())

    total_value = sum(client_portfolio.values())
    if total_value == 0:
        percentages = {spirit: 0.0 for spirit in client_portfolio}
    else:
        percentages = {
            spirit: (value / total_value) * 100 for spirit, value in client_portfolio.items()
        }

    return percentages, total_value


def adjust(value, spirit_name, total_val):
    # Retrieve target weights, price, and units for the spirit
    target_min, target_max = TARGET_WEIGHTS[spirit_name]
    price = PRICES_AND_UNITS[spirit_name]["price"]
    units = PRICES_AND_UNITS[spirit_name]["units"]

    # Determine if the spirit needs adjustment based on the target range
    spirit_pct = value / total_val
    if spirit_pct < target_min:
        return units * price, value + units * price  # Return the adjustment amount and new value
    elif spirit_pct > target_max and value >= units * price:
        return -units * price, value - units * price
    return 0, value


def rebalance(client_portfolio, min_investment, max_investment):
    MAX_ITERATIONS = 100
    iteration = 0
    new_client_portfolio = client_portfolio.copy()

    # Initialize the adjustments
    adjustments = {spirit: 0 for spirit in TARGET_WEIGHTS.keys()}

    while iteration < MAX_ITERATIONS:
        iteration += 1
        adjustments_made = False
        total_val = sum(new_client_portfolio.values())

        for spirit in new_client_portfolio.keys():
            change, new_val = adjust(new_client_portfolio[spirit], spirit, total_val)
            if change != 0:
                adjustments_made = True
                adjustments[spirit] += change
                new_client_portfolio[spirit] = new_val

        # Break the loop if no adjustments were made in this iteration
        if not adjustments_made:
            break

    # Handle min/max investment constraints
    total_val = sum(new_client_portfolio.values())
    if total_val < min_investment:
        # Logic to increase portfolio size
        pass
    elif total_val > max_investment:
        # Logic to decrease portfolio size
        pass

    units_adjustments = {}
    cost_adjustments = {}
    for spirit, change in adjustments.items():
        units = PRICES_AND_UNITS[spirit]["units"]
        price = PRICES_AND_UNITS[spirit]["price"]
        units_change = change / (units * price)
        units_adjustments[spirit] = units_change
        cost_adjustments[spirit] = change

    return {
        "Updated Portfolio": new_client_portfolio,
        "Units Adjustments": units_adjustments,
        "Cost Adjustments": cost_adjustments,
    }


# Testing
client_portfolio = {
    "American Whiskey": 27782.04,
    "Irish Whiskey": 27280.74,
    "Scotch Whisky": 19239.22,
    "Tequila": 0.0,
}
client_min_investment = 50000
client_max_investment = 100000
result = rebalance(client_portfolio, client_min_investment, client_max_investment)

new_client_portfolio = result["Updated Portfolio"]
units_adjustments = result["Units Adjustments"]
cost_adjustments = result["Cost Adjustments"]


display_portfolio(client_portfolio, title="Client Portfolio - original")
display_adjustments(units_adjustments, cost_adjustments)
display_portfolio(new_client_portfolio, title="Client Portfolio - new")
