import xmlrpc.client

from app.config import (
    ODOO_URL,
    ODOO_DB,
    ODOO_USERNAME,
    ODOO_PASSWORD
)


class OdooClient:

    def __init__(self):

        self.common = xmlrpc.client.ServerProxy(
            f"{ODOO_URL}/xmlrpc/2/common"
        )

        self.models = xmlrpc.client.ServerProxy(
            f"{ODOO_URL}/xmlrpc/2/object"
        )

        self.uid = None

    def authenticate(self):

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