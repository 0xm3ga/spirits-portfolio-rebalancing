from constants import TARGET_WEIGHTS


def display_portfolio(
    client_portfolio, title="Client Portfolio", client_id=None, min_val=None, max_val=None
):
    # Compute the percentage allocation for each spirit
    total_value = sum(client_portfolio.values())
    if total_value == 0:
        percentages = {spirit: 0.0 for spirit in client_portfolio}
    else:
        percentages = {
            spirit: (value / total_value) * 100 for spirit, value in client_portfolio.items()
        }

    print()

    # Decorative function to display a title
    def display_title(text):
        print("=" * 80)
        print(text.center(80))
        print("=" * 80)
        print()

    # Display title
    display_title(title)

    # Display client ID if provided
    if client_id:
        print(f"Client ID: {client_id}")
        print("-" * 80)

    # Display the portfolio neatly
    print(
        "{:<20} {:<20} {:<20} {:<20}".format(
            "Spirit", "Value (£)", "Percentage (%)", "Target Range (%)"
        )
    )
    print("-" * 80)
    for spirit, value in client_portfolio.items():
        target_range = f"{TARGET_WEIGHTS[spirit][0]*100:.2f} - {TARGET_WEIGHTS[spirit][1]*100:.2f}"
        print(
            "{:<20} {:<20,.2f} {:<20,.2f} {:<20}".format(
                spirit, value, percentages[spirit], target_range
            )
        )
    print("-" * 80)
    print("{:<20} {:<20,.2f}".format("Total", total_value))

    # Print the min and max values if provided
    if min_val is not None or max_val is not None:
        print("-" * 80)
        if min_val is not None:
            print("{:<20} {:<20,.2f}".format("Min Value", min_val))
        if max_val is not None:
            print("{:<20} {:<20,.2f}".format("Max Value", max_val))

    print("-" * 80)
    print()
    print()


def display_adjustments(units_adjustments, cost_adjustments, title="Adjustments"):
    WIDTH = 80

    print()

    def display_title(text):
        print("=" * WIDTH)
        print(text.center(WIDTH))
        print("=" * WIDTH)
        print()

    # Display title
    display_title(title)

    # Display the headings
    print("{:<25} {:<25} {:<25}".format("Spirit", "Units Adjustments", "Cost Adjustments (£)"))
    print("-" * WIDTH)
    for spirit, units in units_adjustments.items():
        cost = cost_adjustments[spirit]
        print("{:<25} {:<25,.1f} {:<25,.2f}".format(spirit, units, cost))
    print("-" * WIDTH)
    print()
    print()
