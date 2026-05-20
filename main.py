from app.odoo_client import OdooClient


def main():

    client = OdooClient()

    client.authenticate()


if __name__ == "__main__":
    main()