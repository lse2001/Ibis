# odoo_client.py

import xmlrpc.client

from datetime import datetime, timedelta

from app.config import (
    ODOO_URL,
    ODOO_DB,
    ODOO_USERNAME,
    ODOO_PASSWORD
)


class OdooClient:

    def __init__(self):

        # endpoint used for authentication
        self.common = xmlrpc.client.ServerProxy(
            f"{ODOO_URL}/xmlrpc/2/common"
        )

        # endpoint used for querying models/data
        self.models = xmlrpc.client.ServerProxy(
            f"{ODOO_URL}/xmlrpc/2/object"
        )

        self.uid = None

    def authenticate(self):

        # sends credentials to Odoo
        # returns a user id if successful
        self.uid = self.common.authenticate(
            ODOO_DB,
            ODOO_USERNAME,
            ODOO_PASSWORD,
            {}
        )

        if self.uid:
            print(f"Successfully authenticated with Odoo. UID: {self.uid}")
            return True

        print("Authentication failed.")
        return False

    def get_recent_confirmed_orders(self):

        # current time minus 48 hours
        cutoff = datetime.now() - timedelta(hours=48)

        # Odoo expects datetime strings in this format
        cutoff_string = cutoff.strftime("%Y-%m-%d %H:%M:%S")

        # domain = filters
        # only return orders that:
        # 1. are confirmed sales orders
        # 2. were created in last 48h
        # 3. have a customer reference / PO number
        # using date_order because it reflects the quotation/order
        # timestamp shown in the Odoo UI. this is the business-facing
        # order date associated with the sales order workflow.
        domain = [
            ("state", "=", "sale"),
            ("date_order", ">=", cutoff_string),
            ("client_order_ref", "!=", False),
        ]

        # fields = columns/data we want returned
        fields = [
            "name",
            "partner_id",
            "client_order_ref",
            "date_order",
            "create_date",
            "amount_total",
            "order_line",
        ]

        # query the sale.order model
        orders = self.models.execute_kw(
            ODOO_DB,
            self.uid,
            ODOO_PASSWORD,
            "sale.order",
            "search_read",
            [domain],
            {"fields": fields},
        )

        return orders