import xmlrpc.client

from app.config import ODOO_URL


def main():

    # Make sure the URL exists before trying to connect
    if not ODOO_URL:
        print("ODOO_URL is missing from .env")
        return

    # Create connection to Odoo's common XML-RPC endpoint
    common = xmlrpc.client.ServerProxy(
        f"{ODOO_URL}/xmlrpc/2/common"
    )

    try:

        # Ask Odoo for version information
        version_info = common.version()

        print("Successfully connected to Odoo.")
        print(version_info)

    except Exception as error:

        print("Could not connect to Odoo.")
        print(error)


if __name__ == "__main__":
    main()