from app.odoo_client import OdooClient


def main():

    client = OdooClient()

    if not client.authenticate():
        return

    orders = client.get_recent_confirmed_orders()

    # Phase B needs to generate one Part Summary for each matching order.
    #
    # In a normal Odoo workflow, one sale.order can contain multiple
    # sale.order.line records. For example, SO1002 could have both
    # "2x Thermal Bracket" and "1x Composite Panel" attached to the same
    # quotation/order.
    #
    # In this demo sandbox, imported CSV data can also create a slightly
    # different shape: the same order reference may appear multiple times,
    # with each imported record holding one quoted part independently.
    #
    # group_orders_with_parts() handles both cases by grouping matching
    # orders by order reference and customer PO number, then combining all
    # related order line items into one Part Summary.
    grouped_orders = client.group_orders_with_parts(orders)

    print("\nMatching Orders:\n")

    for order in grouped_orders:

        part_summary = ", ".join(order["parts"])

        print(f"Order: {order['name']}")
        print(f"Customer: {order['customer']}")
        print(f"PO Number: {order['po_number']}")
        print(f"Order Date: {order['order_date']}")
        print(f"Part Summary: {part_summary}")
        print("-" * 40)


if __name__ == "__main__":
    main()