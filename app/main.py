from pathlib import Path
import json

from app.odoo_client import OdooClient
from app.emailer import send_order_email

PROCESSED_ORDERS_FILE = "../processed_orders.json"


def get_order_key(order):
    """
    Builds the unique order identifier used for notification tracking.

    The key combines:
    1. the internal Odoo sales order number
    2. the customer PO number

    Example:
    "SO1002|PO-77102"
    """

    return f"{order['name']}|{order['po_number']}"


def send_email_and_record_order(order):
    """
    Sends an email notification for a confirmed order
    if that order has not already been emailed.

    After the email succeeds, the order key is saved
    into the JSON file so future script runs skip it.

    This prevents duplicate notifications while also
    avoiding bugs where an order could be marked as
    emailed before the email successfully sends.
    """

    order_key = get_order_key(order)

    file_path = Path(PROCESSED_ORDERS_FILE)

    # load existing processed order keys
    if file_path.exists():

        with open(file_path, "r") as file:
            processed_orders = json.load(file)

    else:
        processed_orders = []

    # skip duplicate notifications
    if order_key in processed_orders:

        print(
            f"Email already sent for "
            f"{order['name']} - {order['po_number']}"
        )

        return False

    # send the Gmail notification
    send_order_email(order)

    # only record the order after the email succeeds
    processed_orders.append(order_key)

    # overwrite the JSON file with updated processed orders
    with open(file_path, "w") as file:
        json.dump(processed_orders, file, indent=4)

    print(
        f"Email sent and recorded for "
        f"{order['name']} - {order['po_number']}"
    )

    return True


def get_authenticated_client():
    """
    Creates an OdooClient instance and attempts to authenticate
    against the configured Odoo sandbox instance.

    If authentication succeeds, the authenticated client is returned.

    If authentication fails, None is returned so the main program
    can safely stop execution before attempting any Odoo queries.
    """

    client = OdooClient()

    if not client.authenticate():
        return None

    return client


def process_matching_orders(client):
    """
    Retrieves matching confirmed sales orders from Odoo,
    normalizes the order structure, and displays the final
    processed order summaries.

    In a normal Odoo workflow, one sale.order can contain
    multiple sale.order.line records. For example, SO1002
    could have both "2x Thermal Bracket" and
    "1x Composite Panel" attached to the same quotation/order.

    In this demo sandbox, imported CSV data can also create
    a slightly different shape: the same order reference may
    appear multiple times, with each imported record holding
    one quoted part independently.

    group_orders_with_parts() handles both cases by grouping
    matching orders by order reference and customer PO number,
    then combining all related order line items into one
    consolidated Part Summary.
    """

    orders = client.get_recent_confirmed_orders()

    grouped_orders = client.group_orders_with_parts(
        orders
    )

    print("\nMatching Orders:\n")

    for order in grouped_orders:

        part_summary = ", ".join(order["parts"])

        print(f"Order: {order['name']}")
        print(f"Customer: {order['customer']}")
        print(f"PO Number: {order['po_number']}")
        print(f"Order Date: {order['order_date']}")
        print(f"Part Summary: {part_summary}")
        print("-" * 40)

    return grouped_orders


def main():
    """
    Program flow:

    - authenticate and connect to the Odoo sandbox
    - retrieve and normalize matching sales orders
    - generate Part Summaries for each order
    - send Gmail notifications for newly discovered orders
    - record emailed orders in processed_orders.json
      to prevent duplicate notifications
    """

    # authenticate and connect to the Odoo sandbox
    client = get_authenticated_client()

    # stop execution if authentication fails
    if client is None:
        return

    # retrieve and normalize matching sales orders
    grouped_orders = process_matching_orders(client)


    # send notifications for newly discovered orders
    for order in grouped_orders:

        send_email_and_record_order(order)


if __name__ == "__main__":
    main()
