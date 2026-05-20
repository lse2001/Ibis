# main.py
from app.odoo_client import OdooClient


def main():

    client = OdooClient()

    # stop program if auth fails
    if not client.authenticate():
        return

    # fetch matching sales orders
    orders = client.get_recent_confirmed_orders()

    print("\nMatching Orders:\n")

    # loop through returned orders
    for order in orders:

        # partner_id comes back like:
        # [id, customer_name]
        customer_name = order["partner_id"][1]

        print(f"Order: {order['name']}")
        print(f"Customer: {customer_name}")
        print(f"PO Number: {order['client_order_ref']}")
        print(f"Order Date: {order['date_order']}")
        print(f"Total: ${order['amount_total']}")

        print("-" * 40)


if __name__ == "__main__":
    main()